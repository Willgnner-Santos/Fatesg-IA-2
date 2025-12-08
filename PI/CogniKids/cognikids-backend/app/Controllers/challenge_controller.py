# app/Controllers/challenge_controller.py

from flask import Blueprint, request, jsonify
from app.Utils.decorators import token_required
from app.Models.challenge_model import ChallengeModel
from bson.objectid import ObjectId
from app import mongo
from pydantic import BaseModel, ValidationError
from typing import Optional

challenge_blueprint = Blueprint('challenge_bp', __name__)
challenge_model = ChallengeModel()

@challenge_blueprint.route('/challenges/active', methods=['GET'])
@token_required
def get_active_challenges(current_user):
    """
    (ALUNO) Obtém a lista de todos os desafios ativos.
    """
    if current_user['tipo'] != 'aluno':
        return jsonify({'status': 'erro', 'message': 'Apenas alunos podem ver os desafios'}), 403

    try:
        challenges = challenge_model.get_active_challenges()
        student_completions = challenge_model.get_student_completions(str(current_user['_id']))
        completed_challenge_ids = {str(comp['challenge_id']) for comp in student_completions}

        processed_challenges = []
        for challenge in challenges:
            challenge_id_str = str(challenge['_id'])
            challenge_data = {
                '_id': challenge_id_str,
                'title': challenge['title'],
                'description': challenge['description'],
                'points': challenge.get('points', 0),
                'is_completed': challenge_id_str in completed_challenge_ids
            }
            processed_challenges.append(challenge_data)

        return jsonify({'status': 'sucesso', 'data': processed_challenges}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@challenge_blueprint.route('/challenges/<string:challenge_id>/complete', methods=['POST'])
@token_required
def complete_challenge(current_user, challenge_id):
    """
    (ALUNO) Marca um desafio como concluído.
    """
    if current_user['tipo'] != 'aluno':
        return jsonify({'status': 'erro', 'message': 'Apenas alunos podem completar desafios'}), 403

    # Verifica se o desafio existe e está ativo
    challenge = challenge_model.get_challenge_by_id(challenge_id)
    if not challenge or not challenge.get('is_active'):
        return jsonify({'status': 'erro', 'message': 'Desafio não encontrado ou não está mais ativo'}), 404

    result = challenge_model.complete_challenge(str(current_user['_id']), challenge_id)

    if result is None:
        return jsonify({'status': 'informacao', 'message': 'Você já completou este desafio!'}), 200

    return jsonify({
        'status': 'sucesso',
        'message': f"Parabéns! Desafio '{challenge['title']}' concluído com sucesso!"
    }), 201

# --- Rota Administrativa (Exemplo para o futuro) ---
@challenge_blueprint.route('/challenges', methods=['POST'])
@token_required
def create_challenge(current_user):
    """
    (PROFESSOR/ADMIN) Cria um novo desafio.
    """
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403
    
    data = request.get_json()
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'status': 'erro', 'message': 'Título e descrição são obrigatórios'}), 400
        
    data['created_by'] = str(current_user['_id'])
    
    result = challenge_model.create_challenge(data)
    
    return jsonify({
        'status': 'sucesso', 
        'message': 'Desafio criado com sucesso!',
        'challenge_id': str(result.inserted_id)
    }), 201


@challenge_blueprint.route('', methods=['POST'])
@token_required
def create_challenge_root(current_user):
    """Cria novo desafio em /api/challenges (rota raiz do blueprint)."""
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403

    # Validação com Pydantic
    class CreateChallengeModel(BaseModel):
        title: str
        description: str
        class_id: str
        dueDate: Optional[str]

    try:
        payload = request.get_json() or {}
        validated = CreateChallengeModel(**payload)
        data = validated.dict()
    except ValidationError as ve:
        return jsonify({'status': 'erro', 'message': 'Dados inválidos', 'errors': ve.errors()}), 400

    # Autorizar: garantir que o professor é titular da turma
    turma = None
    try:
        turma = mongo.db.classes.find_one({'_id': ObjectId(data['class_id'])})
    except Exception:
        pass

    if not turma or str(turma.get('teacher_id')) != str(current_user['_id']):
        return jsonify({'status': 'erro', 'message': 'Acesso negado: não é professor desta turma'}), 403

    data['created_by'] = str(current_user['_id'])
    result = challenge_model.create_challenge(data)
    return jsonify({'status': 'sucesso', 'message': 'Desafio criado com sucesso!', 'challenge_id': str(result.inserted_id)}), 201


@challenge_blueprint.route('/<string:challenge_id>', methods=['PUT'])
@token_required
def update_challenge(current_user, challenge_id):
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403

    data = request.get_json() or {}
    # Verificar existência e autorização
    existing = challenge_model.get_challenge_by_id(challenge_id)
    if not existing:
        return jsonify({'status': 'erro', 'message': 'Desafio não encontrado'}), 404

    # Verificar se o professor é o criador ou titular da turma
    class_id = existing.get('class_id') or existing.get('class') or existing.get('class_id')
    if class_id:
        turma = mongo.db.classes.find_one({'_id': ObjectId(class_id)})
        if turma and str(turma.get('teacher_id')) != str(current_user['_id']):
            return jsonify({'status': 'erro', 'message': 'Acesso negado: não é professor desta turma'}), 403

    result = challenge_model.update_challenge(challenge_id, data)
    if result.matched_count == 0:
        return jsonify({'status': 'erro', 'message': 'Desafio não encontrado para atualizar'}), 404

    return jsonify({'status': 'sucesso', 'message': 'Desafio atualizado com sucesso'}), 200


@challenge_blueprint.route('/<string:challenge_id>', methods=['DELETE'])
@token_required
def delete_challenge(current_user, challenge_id):
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403

    existing = challenge_model.get_challenge_by_id(challenge_id)
    if not existing:
        return jsonify({'status': 'erro', 'message': 'Desafio não encontrado'}), 404

    # Verificar autorização do professor
    class_id = existing.get('class_id') or existing.get('class')
    if class_id:
        turma = mongo.db.classes.find_one({'_id': ObjectId(class_id)})
        if turma and str(turma.get('teacher_id')) != str(current_user['_id']):
            return jsonify({'status': 'erro', 'message': 'Acesso negado: não é professor desta turma'}), 403

    challenge_model.delete_challenge(challenge_id)
    return jsonify({'status': 'sucesso', 'message': 'Desafio removido com sucesso'}), 200