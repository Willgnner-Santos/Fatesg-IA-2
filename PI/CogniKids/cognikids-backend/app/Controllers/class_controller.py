from flask import request, jsonify, Blueprint
from bson import ObjectId
from app.Utils.decorators import token_required
from app.Models.class_model import Class
from app.Models.grade_model import Grade
from app.Models.feeling_model import Feeling
from app.Models.user_model import User

class_blueprint = Blueprint('class', __name__)
class_model = Class()
grade_model = Grade()
feeling_model = Feeling()
user_model = User()

def _get_class_by_id(class_id):
    if not class_id: return None
    try: return class_model.get_class_by_id(class_id)
    except: return None

# =============================================================================
# SECAO 1: VISUALIZACAO
# =============================================================================

@class_blueprint.route('', methods=['GET'])
@token_required
def get_classes(current_user):
    """Lista turmas com contagem de alunos."""
    try:
        teacher_id = str(current_user['_id'])
        # Se for admin/filtro, poderia expandir aqui, mas foca no professor
        classes = class_model.get_teacher_classes(teacher_id)
        
        processed = []
        for c in classes:
            students = c.get('alunos_ids') or c.get('students') or []
            processed.append({
                '_id': str(c.get('_id')),
                'name': c.get('name') or c.get('nome', 'Sem Nome'),
                'grade': c.get('grade', ''),
                'section': c.get('section', ''),
                'student_count': len(students),
                'is_active': c.get('is_active', True)
            })
        return jsonify({'status': 'sucesso', 'data': processed}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@class_blueprint.route('/<string:class_id>', methods=['GET'])
@token_required
def get_class_details(current_user, class_id):
    """Detalhes de uma turma específica."""
    try:
        turma = _get_class_by_id(class_id)
        if not turma:
            return jsonify({'status': 'erro', 'message': 'Turma não encontrada'}), 404
        
        turma['_id'] = str(turma['_id'])
        turma['teacher_id'] = str(turma['teacher_id'])
        turma['student_count'] = len(turma.get('alunos_ids', []) or [])
        return jsonify({'status': 'sucesso', 'data': turma}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

# =============================================================================
# SECAO 2: RELATORIOS
# =============================================================================

@class_blueprint.route('/<string:class_id>/report', methods=['GET'])
@token_required
def get_class_report(current_user, class_id):
    """Gera relatório de desempenho e bem-estar."""
    try:
        class_data = _get_class_by_id(class_id)
        if not class_data: return jsonify({'status': 'erro', 'message': 'Turma não encontrada'}), 404
        
        # Validação de acesso
        if str(class_data.get('teacher_id')) != str(current_user.get('_id')):
            return jsonify({'status': 'erro', 'message': 'Acesso negado'}), 403
        
        students = class_data.get('alunos_ids') or []
        students_str = [str(s) for s in students]
        
        grades_summary = grade_model.get_class_grades_summary(class_id)
        
        feelings = feeling_model.find_feelings_by_aluno_ids(students_str) if students_str else []
        wellbeing_counts = {}
        for f in feelings:
            s = f.get('sentimento') or 'unknown'
            wellbeing_counts[s] = wellbeing_counts.get(s, 0) + 1
            
        report = {
            'class_id': str(class_data.get('_id')),
            'name': class_data.get('name'),
            'wellbeing': {'total_records': len(feelings), 'counts': wellbeing_counts},
            'grades_summary': grades_summary,
            'student_count': len(students)
        }
        return jsonify({'status': 'sucesso', 'report': report}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

# =============================================================================
# SECAO 3: GERENCIAMENTO (CRIAR, EDITAR, EXCLUIR)
# =============================================================================

@class_blueprint.route('/classes', methods=['POST'])
@token_required
def create_class(current_user):
    """Cria nova turma."""
    try:
        data = request.get_json()
        data['teacher_id'] = current_user['_id']
        # Garante lista vazia de alunos
        if 'alunos_ids' not in data: data['alunos_ids'] = []
        
        result = class_model.create_class(data)
        return jsonify({'status': 'sucesso', 'message': 'Turma criada', '_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@class_blueprint.route('/classes/<string:class_id>', methods=['PUT'])
@token_required
def update_class(current_user, class_id):
    """Atualiza dados da turma."""
    try:
        data = request.get_json()
        result = class_model.update_class(class_id, data)
        if result.modified_count:
            return jsonify({'status': 'sucesso', 'message': 'Turma atualizada'}), 200
        return jsonify({'status': 'sucesso', 'message': 'Nenhuma alteração feita'}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@class_blueprint.route('/classes/<string:class_id>', methods=['DELETE'])
@token_required
def delete_class(current_user, class_id):
    """Desativa uma turma."""
    try:
        # Verifica se tem alunos antes de apagar? Opcional.
        result = class_model.deactivate_class(class_id)
        if result.modified_count:
            return jsonify({'status': 'sucesso', 'message': 'Turma removida'}), 200
        return jsonify({'status': 'erro', 'message': 'Turma não encontrada'}), 404
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

# =============================================================================
# SECAO 4: GESTAO DE ALUNOS NA TURMA
# =============================================================================

@class_blueprint.route('/<string:class_id>/enroll_student', methods=['POST'])
@token_required
def enroll_student(current_user, class_id):
    """Adiciona aluno à turma."""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        if not student_id: return jsonify({'status': 'erro', 'message': 'ID do aluno obrigatório'}), 400
        
        class_model.enroll_student(class_id, student_id)
        # Também atualiza o user para ter o vínculo reverso
        user_model.update_user(student_id, {"turma_id": ObjectId(class_id)})
        
        return jsonify({'status': 'sucesso', 'message': 'Aluno matriculado'}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@class_blueprint.route('/<string:class_id>/remove_student', methods=['POST'])
@token_required
def remove_student(current_user, class_id):
    """Remove aluno da turma."""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        if not student_id: return jsonify({'status': 'erro', 'message': 'ID do aluno obrigatório'}), 400
        
        class_model.remove_student(class_id, student_id)
        user_model.update_user(student_id, {"turma_id": None}) # Remove vínculo
        
        return jsonify({'status': 'sucesso', 'message': 'Aluno removido'}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500