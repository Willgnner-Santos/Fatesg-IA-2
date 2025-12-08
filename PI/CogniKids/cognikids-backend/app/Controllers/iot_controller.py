# app/Controllers/iot_controller.py
from flask import Blueprint, request, jsonify
from app import mongo
from app.Utils.validators import validate_object_id
from bson.objectid import ObjectId
import datetime
import os

# Inicializa o Blueprint
iot_bp = Blueprint('iot_bp', __name__)

@iot_bp.route('/data', methods=['POST'])
def receber_dados_iot():
    """
    Endpoint para receber dados de dispositivos IoT.
    Protegido por chave X-API-Key.
    """
    try:
        # VALIDAÇÃO DA API KEY - Agora usando a variável de ambiente
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('SECRET_API_KEY')
        if not api_key or api_key != expected_key:
            return jsonify({"status": "erro", "message": "API Key inválida ou ausente"}), 401
        
        data = request.get_json()
        if not data or 'dispositivo_id' not in data or 'dados_biometricos' not in data:
            return jsonify({"status": "erro", "message": "Dados ausentes: dispositivo_id e dados_biometricos são obrigatórios"}), 400

        dispositivo_id = data['dispositivo_id']
        dados_biometricos = data['dados_biometricos']

        # Validação do ObjectId
        if not validate_object_id(dispositivo_id):
            return jsonify({"status": "erro", "message": "ID do dispositivo inválido"}), 400

        # Validação básica dos dados biométricos
        if not isinstance(dados_biometricos, dict) or not dados_biometricos:
            return jsonify({"status": "erro", "message": "Dados biométricos devem ser um objeto não vazio"}), 400

        # 1. Verifica se o dispositivo existe e obtém o ID do aluno
        dispositivo = mongo.db.dispositivos.find_one({"_id": ObjectId(dispositivo_id)})
        if not dispositivo:
            return jsonify({"status": "erro", "message": "Dispositivo não registrado"}), 404
        
        aluno_id = dispositivo.get('aluno_id')
        if not aluno_id:
            return jsonify({"status": "erro", "message": "Dispositivo não associado a nenhum aluno"}), 400

        # 2. Cria o novo registro de dados
        novo_registro = {
            "dispositivo_id": ObjectId(dispositivo_id),
            "aluno_id": ObjectId(aluno_id),
            "data_hora": datetime.datetime.utcnow(),
            "dados_biometricos": dados_biometricos,
            "processado": False  # Flag para processamento posterior
        }
        
        # 3. Insere o registro no banco de dados
        resultado = mongo.db.registros_iot.insert_one(novo_registro)
        
        # 4. Atualiza o status do dispositivo (última conexão)
        mongo.db.dispositivos.update_one(
            {"_id": ObjectId(dispositivo_id)},
            {"$set": {
                "ultima_conexao": datetime.datetime.utcnow(), 
                "status": "ativo",
                "ultimo_registro_id": resultado.inserted_id
            }}
        )
        
        return jsonify({
            "status": "sucesso", 
            "message": "Dados recebidos com sucesso!",
            "registro_id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "status": "erro", 
            "message": "Erro interno ao salvar os dados", 
            "error": str(e)
        }), 500

@iot_bp.route('/dispositivos/<aluno_id>', methods=['GET'])
def listar_dispositivos_aluno(aluno_id):
    """Listar dispositivos de um aluno específico"""
    try:
        if not validate_object_id(aluno_id):
            return jsonify({"status": "erro", "message": "ID do aluno inválido"}), 400

        dispositivos = list(mongo.db.dispositivos.find({"aluno_id": ObjectId(aluno_id)}))
        
        # Converter ObjectId para string para serialização JSON
        for dispositivo in dispositivos:
            dispositivo['_id'] = str(dispositivo['_id'])
            dispositivo['aluno_id'] = str(dispositivo['aluno_id'])
        
        return jsonify({
            "status": "sucesso",
            "dispositivos": dispositivos
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "message": "Erro ao buscar dispositivos",
            "error": str(e)
        }), 500

@iot_bp.route('/registros/<aluno_id>', methods=['GET'])
def listar_registros_aluno(aluno_id):
    """Listar registros IoT de um aluno específico"""
    try:
        if not validate_object_id(aluno_id):
            return jsonify({"status": "erro", "message": "ID do aluno inválido"}), 400

        # Parâmetros de paginação opcionais
        limite = request.args.get('limite', 50, type=int)
        pagina = request.args.get('pagina', 1, type=int)
        skip = (pagina - 1) * limite

        registros = list(mongo.db.registros_iot.find(
            {"aluno_id": ObjectId(aluno_id)}
        ).sort("data_hora", -1).skip(skip).limit(limite))
        
        # Converter ObjectId para string
        for registro in registros:
            registro['_id'] = str(registro['_id'])
            registro['dispositivo_id'] = str(registro['dispositivo_id'])
            registro['aluno_id'] = str(registro['aluno_id'])
        
        return jsonify({
            "status": "sucesso",
            "registros": registros,
            "pagina": pagina,
            "limite": limite
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "message": "Erro ao buscar registros",
            "error": str(e)
        }), 500

@iot_bp.route('/crisis-alerts', methods=['GET'])
def get_crisis_alerts():
    """
    Retorna alertas de crise para professores.
    Um alerta de crise é gerado quando:
    - heart_rate > 120 OU
    - eda > 3.0
    """
    try:
        # Aplicar autenticação manualmente
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] if len(request.headers['Authorization'].split(" ")) > 1 else None
        
        if not token:
            return jsonify({"status": "erro", "message": "Token ausente"}), 401
        
        import jwt
        try:
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            current_user = mongo.db.users.find_one({"_id": ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({"status": "erro", "message": "Usuário não encontrado"}), 401
        except Exception:
            return jsonify({"status": "erro", "message": "Token inválido"}), 401
        
        # Verificar se é professor
        if current_user.get('tipo') != 'professor':
            return jsonify({"status": "erro", "message": "Acesso negado. Apenas professores."}), 403
        
        # Buscar turmas do professor
        turmas_ids = current_user.get('turmas_ids', [])
        if not turmas_ids:
            return jsonify({"status": "sucesso", "alerts": []}), 200
        
        # Buscar alunos das turmas do professor
        alunos = list(mongo.db.users.find({
            "tipo": {"$in": ["aluno", "estudante"]},  # Aceitar ambos os tipos
            "turma_id": {"$in": turmas_ids}
        }))
        
        alunos_ids = [aluno['_id'] for aluno in alunos]
        
        # Buscar registros IoT dos últimos 30 minutos que indicam crise
        from datetime import timedelta
        time_threshold = datetime.datetime.utcnow() - timedelta(minutes=30)
        
        registros_crise = list(mongo.db.registros_iot.find({
            "aluno_id": {"$in": alunos_ids},
            "data_hora": {"$gte": time_threshold},
            "$or": [
                {"dados_biometricos.heart_rate": {"$gt": 120}},
                {"dados_biometricos.eda": {"$gt": 3.0}}
            ]
        }).sort("data_hora", -1))
        
        # Formatar alertas
        alerts = []
        for registro in registros_crise:
            aluno = next((a for a in alunos if a['_id'] == registro['aluno_id']), None)
            if aluno:
                alerts.append({
                    "student_id": str(registro['aluno_id']),
                    "student_name": aluno.get('nome', 'Desconhecido'),
                    "heart_rate": registro['dados_biometricos'].get('heart_rate'),
                    "eda": registro['dados_biometricos'].get('eda'),
                    "timestamp": registro['data_hora'].isoformat(),
                    "severity": "high" if (
                        registro['dados_biometricos'].get('heart_rate', 0) > 130 or 
                        registro['dados_biometricos'].get('eda', 0) > 4.0
                    ) else "medium"
                })
        
        return jsonify({
            "status": "sucesso",
            "alerts": alerts,
            "count": len(alerts)
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "erro",
            "message": "Erro ao buscar alertas de crise",
            "error": str(e)
        }), 500