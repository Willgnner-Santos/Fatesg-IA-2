from flask import request, jsonify, Blueprint
from app.Utils.decorators import token_required
from app.Models.feeling_model import Feeling
from app.Models.goal_model import Goal
from app.Models.user_model import User
from app.Models.class_model import Class
from bson.objectid import ObjectId
from app import mongo
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional

student_blueprint = Blueprint('student', __name__)
feeling_model = Feeling()
goal_model = Goal()
user_model = User()
class_model = Class()

@student_blueprint.route('', methods=['POST'])
@token_required
def create_student(current_user):
    """Cria um novo estudante e o associa a uma turma."""
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Apenas professores podem criar alunos'}), 403

    data = request.get_json()
    required_fields = ['nome', 'email', 'senha', 'turma_id']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'erro', 'message': 'Campos obrigatórios (nome, email, senha, turma_id) em falta'}), 400

    # Verificar se o e-mail já existe
    if user_model.find_by_email(data['email']):
        return jsonify({'status': 'erro', 'message': 'Este e-mail já está em uso'}), 409

    # Criar o novo usuário estudante
    student_data = {
        "nome": data['nome'],
        "email": data['email'],
        "senha": data['senha'],
        "tipo": "estudante",
        "turma_id": ObjectId(data['turma_id'])
    }
    student_id = user_model.create_user(student_data)

    # Adicionar o ID do aluno à lista de alunos da turma
    class_model.add_student_to_class(data['turma_id'], str(student_id))

    return jsonify({
        'status': 'sucesso',
        'message': 'Aluno criado e associado à turma com sucesso!',
        'student_id': str(student_id)
    }), 201

@student_blueprint.route('/feelings', methods=['POST'])
@token_required
def add_feeling(current_user):
    if current_user['tipo'] != 'aluno':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado: apenas para alunos'}), 403

    data = request.get_json()
    if not data or not data.get('sentimento') or not data.get('emoji'):
        return jsonify({'status': 'erro', 'message': 'Dados em falta: sentimento e emoji são obrigatórios'}), 400

    feeling_data = {
        "aluno_id": str(current_user['_id']),
        "sentimento": data['sentimento'],
        "emoji": data['emoji'],
        "descricao": data.get('descricao')
    }
    
    feeling_id = feeling_model.create_feeling(feeling_data)

    return jsonify({
        'status': 'sucesso',
        'message': 'Sentimento registado com sucesso!',
        'feeling_id': str(feeling_id.inserted_id)
    }), 201

@student_blueprint.route('/<string:student_id>/goals', methods=['GET'])
@token_required
def get_student_goals(current_user, student_id):
    is_owner = str(current_user['_id']) == student_id
    is_teacher = current_user['tipo'] == 'professor'
    is_parent = current_user['tipo'] == 'pai' and student_id in [str(id) for id in current_user.get('filhos_ids', [])]

    if not (is_owner or is_teacher or is_parent):
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403

    try:
        goals = goal_model.find_by_student_id(student_id)
        for goal in goals:
            goal['_id'] = str(goal['_id'])
            goal['student_id'] = str(goal['student_id'])
        return jsonify({'status': 'sucesso', 'data': goals}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': f'Erro ao buscar metas: {e}'}), 500

@student_blueprint.route('/goals', methods=['POST'])
@token_required
def create_student_goal(current_user):
    if current_user['tipo'] not in ['professor', 'pai']:
        return jsonify({'status': 'erro', 'message': 'Apenas professores ou pais podem criar metas'}), 403
        
    data = request.get_json()
    required_fields = ['student_id', 'title', 'description', 'deadline']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'erro', 'message': 'Campos obrigatórios em falta'}), 400

    try:
        result = goal_model.create_goal(data)
        return jsonify({
            'status': 'sucesso',
            'message': 'Meta criada com sucesso!',
            'goal_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({'status': 'erro', 'message': f'Erro ao criar meta: {e}'}), 500

@student_blueprint.route('/<string:student_id>', methods=['PUT'])
@token_required
def update_student(current_user, student_id):
    """Atualiza os dados de um estudante."""
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Apenas professores podem editar alunos'}), 403

    # Validação de dados com Pydantic
    class StudentUpdateModel(BaseModel):
        nome: Optional[str]
        email: Optional[EmailStr]
        turma_id: Optional[str]

    try:
        payload = request.get_json() or {}
        validated = StudentUpdateModel(**payload)
        data = validated.dict(exclude_none=True)
    except ValidationError as ve:
        return jsonify({'status': 'erro', 'message': 'Dados inválidos', 'errors': ve.errors()}), 400
    
    # Lógica de autorização: verificar se o professor tem permissão sobre este aluno
    # (Esta parte é crucial e deve ser implementada com cuidado)

    # Remover campos que não devem ser atualizados diretamente por este endpoint
    data.pop('senha', None)
    data.pop('tipo', None)
    
    try:
        # Autorizar: garantir que o professor atual leciona a turma do aluno
        student = mongo.db.users.find_one({"_id": ObjectId(student_id)})
        if not student:
            return jsonify({'status': 'erro', 'message': 'Aluno não encontrado'}), 404

        turma_id = student.get('turma_id') or student.get('class_id')
        if turma_id:
            # garantir ObjectId
            turma = mongo.db.classes.find_one({"_id": ObjectId(turma_id)})
            if turma and turma.get('teacher_id') and str(turma.get('teacher_id')) != str(current_user['_id']):
                return jsonify({'status': 'erro', 'message': 'Acesso negado: não é professor desta turma'}), 403

        result = user_model.update_user(student_id, data)
        if getattr(result, 'matched_count', 0) == 0:
            return jsonify({'status': 'erro', 'message': 'Aluno não encontrado'}), 404

        return jsonify({
            'status': 'sucesso',
            'message': 'Dados do aluno atualizados com sucesso!'
        }), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': f'Erro ao atualizar aluno: {e}'}), 500


@student_blueprint.route('/<string:student_id>', methods=['DELETE'])
@token_required
def delete_student(current_user, student_id):
    """Remove um estudante do sistema e atualiza a turma correspondente."""
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Apenas professores podem remover alunos'}), 403

    try:
        student = mongo.db.users.find_one({"_id": ObjectId(student_id)})
        if not student:
            return jsonify({'status': 'erro', 'message': 'Aluno não encontrado'}), 404

        turma_id = student.get('turma_id') or student.get('class_id')
        if turma_id:
            turma = mongo.db.classes.find_one({"_id": ObjectId(turma_id)})
            if turma and turma.get('teacher_id') and str(turma.get('teacher_id')) != str(current_user['_id']):
                return jsonify({'status': 'erro', 'message': 'Acesso negado: não é professor desta turma'}), 403

            # Remover o aluno da turma (tentar ambos campos 'students' e 'alunos_ids')
            mongo.db.classes.update_one({"_id": ObjectId(turma_id)}, {"$pull": {"students": ObjectId(student_id)}})
            mongo.db.classes.update_one({"_id": ObjectId(turma_id)}, {"$pull": {"alunos_ids": ObjectId(student_id)}})

        # Remover o aluno
        mongo.db.users.delete_one({"_id": ObjectId(student_id)})

        return jsonify({'status': 'sucesso', 'message': 'Aluno removido com sucesso'}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': f'Erro ao remover aluno: {e}'}), 500