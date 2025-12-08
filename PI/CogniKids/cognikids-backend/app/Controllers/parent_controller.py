from flask import request, jsonify, Blueprint
from app.Utils.decorators import token_required
from app.Models.user_model import User
from app.Models.feeling_model import Feeling

parent_blueprint = Blueprint('parent', __name__)
user_model = User()
feeling_model = Feeling()

@parent_blueprint.route('/link-child', methods=['POST'])
@token_required
def link_child(current_user):
    """
    Associar filho ao responsável
    ---
    tags:
      - Responsável
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - child_email
          properties:
            child_email:
              type: string
              example: "filho@escola.com"
    responses:
      200:
        description: Filho associado com sucesso
        schema:
          type: object
          properties:
            status:
              type: string
              example: "sucesso"
            message:
              type: string
              example: "Aluno João associado com sucesso!"
      400:
        description: Email do filho em falta
      403:
        description: Acesso não autorizado
      404:
        description: Aluno não encontrado
    """
    if current_user['tipo'] != 'pai':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403

    data = request.get_json()
    child_email = data.get('child_email')
    if not child_email:
        return jsonify({'status': 'erro', 'message': 'Email do filho em falta'}), 400

    child = user_model.find_user_by_email(child_email)
    if not child or child['tipo'] != 'aluno':
        return jsonify({'status': 'erro', 'message': 'Aluno não encontrado com este email'}), 404

    user_model.link_child_to_parent(str(current_user['_id']), str(child['_id']))

    return jsonify({'status': 'sucesso', 'message': f'Aluno {child["nome"]} associado com sucesso!'}), 200