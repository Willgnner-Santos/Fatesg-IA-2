from flask import request, jsonify, Blueprint
from app.Utils.decorators import token_required
from app.Models.grade_model import Grade
from app.Models.class_model import Class
from app.Models.user_model import User
from app.Controllers.notification_controller import NotificationService
from bson.objectid import ObjectId

grade_blueprint = Blueprint('grade', __name__)
grade_model = Grade()
class_model = Class()
user_model = User()

@grade_blueprint.route('/assignments', methods=['POST'])
@token_required
def create_assignment(current_user):
    """
    Criar uma nova avaliação
    ---
    tags:
      - Notas e Avaliações
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - type
            - class_id
            - subject
            - max_score
          properties:
            title:
              type: string
              example: "Prova de Matemática - Bimestre 1"
            type:
              type: string
              enum: ["prova", "trabalho", "participacao", "atividade", "projeto"]
              example: "prova"
            class_id:
              type: string
              example: "507f1f77bcf86cd799439012"
            subject:
              type: string
              example: "Matemática"
            max_score:
              type: number
              format: float
              example: 10.0
            description:
              type: string
              example: "Prova covering chapters 1-5"
            due_date:
              type: string
              format: date-time
              example: "2024-02-15T23:59:00Z"
            weight:
              type: number
              format: float
              example: 2.0
    responses:
      201:
        description: Avaliação criada com sucesso
        schema:
          type: object
          properties:
            status:
              type: string
              example: "sucesso"
            message:
              type: string
              example: "Avaliação criada com sucesso!"
            assignment_id:
              type: string
              example: "507f1f77bcf86cd799439013"
      400:
        description: Dados em falta
      403:
        description: Acesso não autorizado
    """
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Apenas professores podem criar avaliações'}), 403

    data = request.get_json()
    required_fields = ['title', 'type', 'class_id', 'subject', 'max_score']
    
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'erro', 'message': 'Campos obrigatórios em falta'}), 400

    class_data = class_model.get_class_by_id(data['class_id'])
    if not class_data:
        return jsonify({'status': 'erro', 'message': 'Turma não encontrada'}), 404
    
    if str(class_data['teacher_id']) != str(current_user['_id']):
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403

    data['created_by'] = str(current_user['_id'])
    result = grade_model.create_assignment(data)
    
    return jsonify({
        'status': 'sucesso',
        'message': 'Avaliação criada com sucesso!',
        'assignment_id': str(result.inserted_id)
    }), 201

@grade_blueprint.route('/classes/<class_id>/assignments', methods=['GET'])
@token_required
def get_class_assignments(current_user, class_id):
    """Obter todas as tarefas de uma turma"""
    try:
        # Verificar se o usuário tem acesso à turma
        assignments = grade_model.get_assignments_by_class(class_id)
        
        return jsonify({
            'status': 'sucesso',
            'dados': assignments
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'message': str(e)
        }), 500