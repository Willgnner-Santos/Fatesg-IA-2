from flask import Blueprint, request, jsonify
# Remova a importação de flask_jwt_extended se não for usada diretamente aqui
# from flask_jwt_extended import jwt_required, get_jwt_identity
from app.Utils.decorators import token_required # Supondo que você use seu decorator personalizado
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
import datetime

# Inicializa o Blueprint
support_kit_bp = Blueprint('support_kit_bp', __name__)

# Conexão com o DB (Se estiver a usar a fábrica de aplicação, o 'mongo' virá do app/__init__.py)
client = MongoClient(os.getenv('MONGO_URI'))
db = client.get_database("cognikidsDB")

# Coleções
support_kits_collection = db.support_kits
users_collection = db.users

@support_kit_bp.route('/<string:aluno_id>', methods=['POST', 'PUT'])
@token_required # Usando o decorator personalizado
def upsert_support_kit(current_user, aluno_id): # current_user é injetado pelo decorator
    """
    Cria ou atualiza o Kit de Apoio de um aluno.
    Apenas o pai/responsável associado pode executar esta ação.
    """
    # A verificação de tipo de utilizador e permissão é crucial
    if current_user.get('tipo') != 'pai' or ObjectId(aluno_id) not in current_user.get('filhos_ids', []):
        return jsonify({"msg": "Acesso não autorizado"}), 403

    data = request.get_json()
    
    kit_data = {
        "aluno_id": ObjectId(aluno_id),
        "neurodivergencia": data.get("neurodivergencia", ""), # <<< CAMPO ADICIONADO
        "interesses": data.get("interesses", []),
        "sensibilidades": data.get("sensibilidades", []),
        "estrategias_calmantes": data.get("estrategias_calmantes", ""),
        "contatos_emergencia": data.get("contatos_emergencia", []),
        "last_updated": datetime.datetime.utcnow(),
        "updated_by": ObjectId(current_user['_id'])
    }

    support_kits_collection.update_one(
        {"aluno_id": ObjectId(aluno_id)},
        {"$set": kit_data},
        upsert=True
    )

    return jsonify({"msg": "Kit de Apoio atualizado com sucesso!"}), 200


@support_kit_bp.route('/<string:aluno_id>', methods=['GET'])
@token_required
def get_support_kit(current_user, aluno_id):
    """
    Consulta o Kit de Apoio de um aluno.
    Acessível por professores do aluno e seus responsáveis.
    """
    aluno_id_obj = ObjectId(aluno_id)
    
    # Verificação de permissão
    is_responsavel = current_user.get('tipo') == 'pai' and aluno_id_obj in current_user.get('filhos_ids', [])
    
    # Para o professor, a verificação precisa ser mais robusta.
    # Idealmente, o professor teria uma lista de alunos_ids
    is_professor = current_user.get('tipo') == 'professor' # Simplificado por agora
    
    if not is_responsavel and not is_professor:
        return jsonify({"msg": "Acesso não autorizado"}), 403

    kit = support_kits_collection.find_one({"aluno_id": aluno_id_obj})
    
    if not kit:
        return jsonify({"msg": "Kit de Apoio não encontrado para este aluno."}), 404
        
    # Converte ObjectId para string para ser serializável em JSON
    kit['_id'] = str(kit['_id'])
    kit['aluno_id'] = str(kit['aluno_id'])
    kit['updated_by'] = str(kit['updated_by'])
    
    return jsonify(kit), 200