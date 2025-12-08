# app/Controllers/forum_controller.py

from flask import Blueprint, request, jsonify
from app.Utils.decorators import token_required
from app.Models.forum_model import ForumModel
from bson.objectid import ObjectId

forum_blueprint = Blueprint('forum_bp', __name__)
forum_model = ForumModel()

@forum_blueprint.route('/forum/topics', methods=['GET'])
@token_required
def get_all_topics(current_user):
    """Obter todos os tópicos do fórum."""
    try:
        topics = forum_model.get_all_topics()
        for topic in topics:
            topic['_id'] = str(topic['_id'])
            topic['author_id'] = str(topic['author_id'])
            for reply in topic.get('replies', []):
                reply['reply_id'] = str(reply['reply_id'])
                reply['author_id'] = str(reply['author_id'])
        return jsonify({'status': 'sucesso', 'data': topics}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@forum_blueprint.route('/forum/topics', methods=['POST'])
@token_required
def create_topic(current_user):
    """Criar um novo tópico no fórum."""
    if current_user['tipo'] not in ['professor', 'pai']:
        return jsonify({'status': 'erro', 'message': 'Apenas professores e pais podem criar tópicos'}), 403

    data = request.get_json()
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'status': 'erro', 'message': 'Título e conteúdo são obrigatórios'}), 400

    topic_data = {
        'title': data['title'],
        'content': data['content'],
        'author_id': str(current_user['_id']),
        'author_name': current_user['nome'],
        'author_type': current_user['tipo']
    }
    
    result = forum_model.create_topic(topic_data)
    return jsonify({
        'status': 'sucesso',
        'message': 'Tópico criado com sucesso!',
        'topic_id': str(result.inserted_id)
    }), 201

@forum_blueprint.route('/forum/topics/<string:topic_id>/reply', methods=['POST'])
@token_required
def add_reply_to_topic(current_user, topic_id):
    """Adicionar uma resposta a um tópico."""
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'status': 'erro', 'message': 'Conteúdo da resposta é obrigatório'}), 400
        
    topic = forum_model.get_topic_by_id(topic_id)
    if not topic:
        return jsonify({'status': 'erro', 'message': 'Tópico não encontrado'}), 404

    reply_data = {
        'content': data['content'],
        'author_id': str(current_user['_id']),
        'author_name': current_user['nome'],
        'author_type': current_user['tipo']
    }
    
    forum_model.add_reply(topic_id, reply_data)
    return jsonify({'status': 'sucesso', 'message': 'Resposta adicionada com sucesso!'}), 201