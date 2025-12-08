from flask import jsonify, Blueprint, request
from app.Utils.decorators import token_required
from app.Models.feeling_model import Feeling
from app import mongo  # Importar mongo para consultar o aluno
from bson.objectid import ObjectId # Importar ObjectId

from app.Models.user_model import User
from app.Models.class_model import Class
import datetime
teacher_blueprint = Blueprint('teacher', __name__)
feeling_model = Feeling()
user_model = User()
class_model = Class()

@teacher_blueprint.route('/feelings/all', methods=['GET'])
@token_required
def get_all_feelings(current_user):
    # ... (código existente deste endpoint) ...
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado: apenas para professores'}), 403

    all_feelings = feeling_model.find_all_feelings()

    for feeling in all_feelings:
        feeling['_id'] = str(feeling['_id'])
        feeling['aluno_id'] = str(feeling['aluno_id'])

    return jsonify({'status': 'sucesso', 'data': all_feelings}), 200


# Endpoint: Buscar sentimentos de um aluno especifico

@teacher_blueprint.route('/students/<string:student_id>/feelings', methods=['GET'])
@token_required
def get_student_feelings(current_user, student_id):
    """
    Busca os sentimentos de um aluno específico.
    Acessível por professores e pelo pai/responsável do aluno.
    ---
    tags:
      - Professor
      - Responsável
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: student_id
        required: true
        schema:
          type: string
    responses:
      200:
        description: Lista de sentimentos do aluno
      403:
        description: Acesso não autorizado
      404:
        description: Aluno não encontrado
    """
    try: # Adicionar try/except para ObjectId
        student_id_obj = ObjectId(student_id)
    except:
        return jsonify({'status': 'erro', 'message': 'ID do aluno inválido'}), 400
        
    has_access = False

    # Cenario 1: O utilizador e um professor
    if current_user['tipo'] == 'professor':
        # Verifica se o professor tem acesso a turma do aluno
        student = mongo.db.users.find_one({"_id": student_id_obj, "tipo": "estudante"})
        if student and student.get('turma_id'):
            # Verifica se a turma do aluno esta na lista de turmas do professor
            if student.get('turma_id') in current_user.get('turmas_ids', []):
                has_access = True
        else:
            has_access = False
    
    # Cenário 2: O utilizador é um pai/responsável
    if current_user['tipo'] == 'pai':
        if student_id_obj in current_user.get('filhos_ids', []):
            has_access = True

    if not has_access:
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado para ver os sentimentos deste aluno'}), 403

    # Busca os sentimentos do aluno específico
    student_feelings = feeling_model.find_feelings_by_aluno_id(student_id)
    
    if not student_feelings:
        return jsonify({'status': 'sucesso', 'data': [], 'message': 'Nenhum sentimento registado para este aluno'}), 200

    for feeling in student_feelings:
        feeling['_id'] = str(feeling['_id'])
        feeling['aluno_id'] = str(feeling['aluno_id'])

    return jsonify({'status': 'sucesso', 'data': student_feelings}), 200

# Endpoint: Listar Alunos do Professor

@teacher_blueprint.route('/<string:teacher_id>/students', methods=['GET'])
@token_required
def get_teacher_students(current_user, teacher_id):
    """
    Retorna a lista de alunos das turmas de um professor específico.
    Acessível apenas pelo próprio professor.
    ---
    tags:
      - Professor
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: teacher_id
        required: true
        schema:
          type: string
        description: ID do professor
    responses:
      200:
        description: Lista de alunos do professor
        schema:
          type: object
          properties:
            status:
              type: string
              example: sucesso
            data:
              type: array
              items:
                type: object
      403:
        description: Acesso não autorizado
      404:
        description: Professor não encontrado
    """
    try:
        # Verifica se o usuário logado é o próprio professor
        if str(current_user.get('_id')) != teacher_id:
            return jsonify({
                'status': 'erro',
                'message': 'Acesso não autorizado: você só pode ver seus próprios alunos'
            }), 403
        
        # Verifica se o usuário é professor
        if current_user.get('tipo') != 'professor':
            return jsonify({
                'status': 'erro',
                'message': 'Acesso não autorizado: apenas professores podem acessar esta rota'
            }), 403
        
        # Busca as turmas do professor
        turmas_ids = current_user.get('turmas_ids', [])
        
        if not turmas_ids:
            return jsonify({
                'status': 'sucesso',
                'data': [],
                'message': 'Nenhuma turma atribuída a este professor'
            }), 200
        
        # Busca todos os alunos dessas turmas
        alunos = []
        
        # Converte IDs para ObjectId se necessário
        turmas_ids_obj = []
        for turma_id in turmas_ids:
            if isinstance(turma_id, str):
                turmas_ids_obj.append(ObjectId(turma_id))
            else:
                turmas_ids_obj.append(turma_id)
        
        # Busca alunos no banco de dados
        # Aceita multiplos tipos de usuario (estudante, aluno, student)
        students_cursor = mongo.db.users.find({
            'tipo': {'$in': ['estudante', 'aluno', 'student']},
            'turma_id': {'$in': turmas_ids_obj}
        })
        
        for student in students_cursor:
            # Remove informações sensíveis
            student.pop('senha', None)
            student.pop('password', None)
            
            # Converte ObjectId para string
            student['_id'] = str(student['_id'])
            if 'turma_id' in student:
                student['turma_id'] = str(student['turma_id'])
            
            alunos.append(student)
        
        return jsonify({
            'status': 'sucesso',
            'data': alunos,
            'total': len(alunos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'message': f'Erro ao buscar alunos: {str(e)}'
        }), 500


@teacher_blueprint.route('/crisis_alerts', methods=['GET'])
@token_required
def get_crisis_alerts(current_user):
    """
    (PROFESSOR) Verifica alunos em crise (dados biométricos recentes).
    Busca dados não processados dos últimos 5 minutos.
    """
    try:
        teacher_id = str(current_user['_id'])
        
        # 1. Encontrar todos os alunos deste professor
        
        # Buscar documento do professor
        teacher_doc = user_model.find_user_by_id(teacher_id)
        
        if not teacher_doc:
            return jsonify({'status': 'erro', 'message': 'Professor nao encontrado'}), 404
            
        turmas_ids = teacher_doc.get('turmas_ids', [])
        student_object_ids = set() 

        for class_id in turmas_ids:
            
            # Buscar turma pelo ID
            turma = class_model.get_class_by_id(class_id)

            if turma:
                # Funde as duas listas (a do populate e a do app)
                for sid in turma.get('students', []):
                    student_object_ids.add(ObjectId(sid))
                for sid in turma.get('alunos_ids', []):
                    student_object_ids.add(ObjectId(sid))
        
        if not student_object_ids:
            return jsonify({'status': 'sucesso', 'data': []}), 200 # Professor não tem alunos

        # 2. Definir a janela de tempo (últimos 5 minutos)
        time_window = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)

        # 3. Consultar o Data Mart (alerts) - Crises detectadas pela IA
        query = {
            "student_id": {"$in": list(student_object_ids)},
            "data_hora": {"$gte": time_window}
        }
        crisis_alerts = list(mongo.db.alerts.find(query).sort('data_hora', -1))
        
        if not crisis_alerts:
            return jsonify({'status': 'sucesso', 'data': []}), 200 # Nenhuma crise detectada

        # 4. Processar alertas de crise (já validados pela IA)
        alunos_em_crise = {}

        for alert in crisis_alerts:
            aluno_id_str = str(alert.get('student_id'))
            
            # Evita duplicatas (pega apenas o alerta mais recente por aluno)
            if aluno_id_str not in alunos_em_crise:
                aluno_doc = user_model.find_user_by_id(aluno_id_str)
                
                # Dados biométricos podem estar em 'dados_biometricos' ou diretamente no alert
                dados_bio = alert.get('dados_biometricos', {})
                bpm = dados_bio.get('bpm', dados_bio.get('heart_rate', alert.get('bpm', 0)))
                gsr = dados_bio.get('gsr', alert.get('gsr', 0))

                alunos_em_crise[aluno_id_str] = {
                    "aluno_id": aluno_id_str,
                    "nome": aluno_doc.get('nome') if aluno_doc else alert.get('student_name', 'Aluno Desconhecido'),
                    "heart_rate": bpm,
                    "gsr": gsr,
                    "timestamp": alert.get('data_hora'),
                    "motivo": alert.get('motivo', 'Detecção ML')
                }

        # 5. Retornar a lista de alunos em crise (validados pela IA)
        return jsonify({'status': 'sucesso', 'data': list(alunos_em_crise.values())}), 200

    except Exception as e:
        return jsonify({'status': 'erro', 'message': f'Erro interno do servidor: {str(e)}'}), 500

# Endpoint: Historico de Alertas de um Aluno

@teacher_blueprint.route('/students/<string:student_id>/alerts_history', methods=['GET'])
@token_required
def get_student_alerts_history(current_user, student_id):
    """
    (PROFESSOR) Busca o histórico de alertas/crises de um aluno específico.
    Retorna os últimos 30 dias de alertas para exibição em gráfico.
    GET /api/teachers/students/<student_id>/alerts_history
    """
    try:
        if current_user.get('tipo') != 'professor':
            return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403
        
        # Validar student_id
        try:
            student_id_obj = ObjectId(student_id)
        except:
            return jsonify({'status': 'erro', 'message': 'ID do aluno inválido'}), 400
        
        # Buscar dados do aluno
        aluno = mongo.db.users.find_one({'_id': student_id_obj})
        if not aluno:
            return jsonify({'status': 'erro', 'message': 'Aluno não encontrado'}), 404
        
        # Buscar alertas dos últimos 30 dias
        data_limite = datetime.datetime.utcnow() - datetime.timedelta(days=30)
        
        alertas = list(mongo.db.alerts.find({
            'aluno_id': student_id_obj,
            'data_hora': {'$gte': data_limite}
        }).sort('data_hora', 1))  # Ordenar por data crescente
        
        # Processar alertas para o frontend
        historico = []
        for alerta in alertas:
            dados_bio = alerta.get('dados_biometricos', {})
            historico.append({
                '_id': str(alerta['_id']),
                'data_hora': alerta.get('data_hora').isoformat() if alerta.get('data_hora') else None,
                'bpm': dados_bio.get('bpm', dados_bio.get('heart_rate', 0)),
                'gsr': dados_bio.get('gsr', 0),
                'temperature': dados_bio.get('temperature', 0),
                'severity': alerta.get('severity', 'medium'),
                'motivo': alerta.get('motivo', ''),
                'resolvido': alerta.get('resolvido', False),
                'ml_confidence': alerta.get('ml_confidence', 0)
            })
        
        return jsonify({
            'status': 'sucesso',
            'data': {
                'aluno_nome': aluno.get('nome', 'Desconhecido'),
                'aluno_id': student_id,
                'total_alertas': len(historico),
                'historico': historico
            }
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'erro', 'message': f'Erro ao buscar histórico: {str(e)}'}), 500

# ==================== NOVO ENDPOINT: Listar TODOS os Alunos do Professor Logado ====================

@teacher_blueprint.route('/all_students', methods=['GET'])
@token_required
def get_all_students_teacher(current_user):
    """
    (PROFESSOR) Obtém TODOS os alunos de TODAS as turmas do professor logado.
    Usado pelo dashboard principal do professor.
    GET /api/teachers/all_students
    """
    try:
        # Verifica se o usuário é professor
        if current_user.get('tipo') != 'professor':
            return jsonify({
                'status': 'erro',
                'message': 'Acesso não autorizado: apenas professores podem acessar esta rota'
            }), 403

        # Busca as turmas do professor logado
        turmas_ids = current_user.get('turmas_ids', [])

        if not turmas_ids:
            return jsonify({
                'status': 'sucesso',
                'data': [],
                'message': 'Nenhuma turma atribuída a este professor'
            }), 200

        # Converte IDs para ObjectId se necessário
        turmas_ids_obj = []
        for turma_id in turmas_ids:
            if isinstance(turma_id, str):
                turmas_ids_obj.append(ObjectId(turma_id))
            else:
                turmas_ids_obj.append(turma_id)

        # Busca todos os alunos dessas turmas
        # CORREÇÃO: Aceitar múltiplos tipos (estudante, aluno, student)
        students_cursor = mongo.db.users.find({
            'tipo': {'$in': ['estudante', 'aluno', 'student']},
            'turma_id': {'$in': turmas_ids_obj}
        })

        alunos = []
        for student in students_cursor:
            # Remove informações sensíveis
            student.pop('senha', None)
            student.pop('password', None)

            # Converte ObjectId para string
            student['_id'] = str(student['_id'])
            if 'turma_id' in student:
                student['turma_id'] = str(student['turma_id'])

            alunos.append(student)

        return jsonify({
            'status': 'sucesso',
            'data': alunos,
            'total': len(alunos)
        }), 200

    except Exception as e:
        print(f'Erro ao buscar todos os alunos do professor: {e}')
        return jsonify({
            'status': 'erro',
            'message': f'Erro interno do servidor: {str(e)}'
        }), 500


@teacher_blueprint.route('/students_average_grade', methods=['GET'])
@token_required
def get_students_average_grade(current_user):
    """
    Calcula a média de notas de todos os alunos do professor.
    """
    try:
        from app.Models.grade_model import Grade
        grade_model = Grade()
        
        teacher_id = str(current_user['_id'])
        
        # 1. Buscar alunos do professor
        teacher_doc = user_model.find_user_by_id(teacher_id)
        if not teacher_doc:
            return jsonify({'status': 'erro', 'message': 'Professor não encontrado'}), 404
        
        turmas_ids = teacher_doc.get('turmas_ids', [])
        student_ids = []
        
        for turma_id in turmas_ids:
            turma = class_model.get_class_by_id(turma_id)
            if turma:
                for aluno_id in turma.get('alunos_ids', []):
                    student_ids.append(str(aluno_id))
        
        if not student_ids:
            return jsonify({'status': 'sucesso', 'data': {'average': None, 'count': 0}}), 200
        
        # 2. Buscar todas as notas dos alunos
        all_grades = []
        for student_id in student_ids:
            try:
                grades = list(mongo.db.grades.find({'student_id': ObjectId(student_id)}))
                for grade in grades:
                    score = grade.get('score')
                    if score is not None and isinstance(score, (int, float)) and score >= 0:
                        all_grades.append(float(score))
            except:
                continue
        
        if not all_grades:
            return jsonify({'status': 'sucesso', 'data': {'average': None, 'count': 0}}), 200
        
        # 3. Calcular média
        average = sum(all_grades) / len(all_grades)
        
        return jsonify({
            'status': 'sucesso',
            'data': {
                'average': round(average, 1),
                'count': len(all_grades),
                'students': len(student_ids)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'message': f'Erro ao calcular média: {str(e)}'
        }), 500


# ==================== HISTÓRICO DE ALERTAS ====================

@teacher_blueprint.route('/students/<string:student_id>/alert_history', methods=['GET'])
@token_required
def get_student_alert_history(current_user, student_id):
    """
    Busca o histórico de alertas de crise de um aluno específico.
    Retorna os últimos 30 dias de alertas.
    ---
    tags:
      - Professor
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: student_id
        required: true
        schema:
          type: string
        description: ID do aluno
    responses:
      200:
        description: Histórico de alertas
      403:
        description: Acesso não autorizado
      404:
        description: Aluno não encontrado
    """
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403
    
    try:
        # Verifica se o aluno existe
        try:
            student = mongo.db.users.find_one({'_id': ObjectId(student_id), 'tipo': 'estudante'})
        except:
            return jsonify({'status': 'erro', 'message': 'ID de aluno inválido'}), 400
        
        if not student:
            return jsonify({'status': 'erro', 'message': 'Aluno não encontrado'}), 404
        
        # Calcula data de 30 dias atrás
        thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        
        # Busca alertas do aluno nos últimos 30 dias
        alerts = list(mongo.db.alerts.find({
            'student_id': ObjectId(student_id),
            'data_hora': {'$gte': thirty_days_ago}
        }).sort('data_hora', -1))
        
        # Formata os alertas para resposta
        formatted_alerts = []
        for alert in alerts:
            # Extrai dados biometricos (pode estar em dados_biometricos ou campos raiz)
            dados_bio = alert.get('dados_biometricos', {})
            bpm = dados_bio.get('bpm', alert.get('bpm', 0))
            gsr = dados_bio.get('gsr', alert.get('gsr', 0))
            movement = dados_bio.get('movement_score', alert.get('movement_score', 0))
            
            formatted_alerts.append({
                '_id': str(alert.get('_id')),
                'data_hora': alert.get('data_hora').isoformat() if alert.get('data_hora') else None,
                'severity': alert.get('severity', 'medium'),
                'bpm': bpm,
                'gsr': gsr,
                'movement_score': movement,
                'motivo': alert.get('motivo', 'Nao especificado'),
                'resolvido': alert.get('resolvido', False)
            })
        
        return jsonify({
            'success': True,
            'student_name': student.get('nome', 'Desconhecido'),
            'alerts': formatted_alerts,
            'count': len(formatted_alerts)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao buscar histórico: {str(e)}'
        }), 500
