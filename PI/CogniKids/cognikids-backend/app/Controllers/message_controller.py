from flask import request, jsonify, Blueprint
from app.Utils.decorators import token_required
from app.Models.message_model import Message
from app.Models.user_model import User
from app.Controllers.notification_controller import NotificationService
from bson.objectid import ObjectId 

message_blueprint = Blueprint('message_bp', __name__)
message_model = Message()
user_model = User()

@message_blueprint.route('/message', methods=['POST'])
@token_required
def send_message(current_user):
    """ 
    Enviar mensagem entre usuários
    """
    data = request.get_json()
    
    if not data or not data.get('to_user_id') or not data.get('content'):
        return jsonify({'status': 'erro', 'message': 'Destinatário e conteúdo são obrigatórios'}), 400
    
    # Verificar se destinatário existe
    to_user = user_model.find_user_by_id(data['to_user_id'])
    if not to_user:
        return jsonify({'status': 'erro', 'message': 'Destinatário não encontrado'}), 404
    
    # Verificar regras de comunicação
    if current_user['tipo'] == to_user['tipo']:
        return jsonify({'status': 'erro', 'message': 'Só é permitido enviar mensagens para perfis diferentes'}), 403
    
    # Criar mensagem
    result = message_model.create_message(
        str(current_user['_id']),
        data['to_user_id'],
        data['content'],
        data.get('message_type', 'text'),
        data.get('priority', 'normal')
    )
    
    NotificationService.notify_new_message(
        data['to_user_id'],
        current_user['nome'],
        data['content'],
        str(result.inserted_id)
    )
    
    return jsonify({
        'status': 'sucesso',
        'message': 'Mensagem enviada com sucesso!',
        'message_id': str(result.inserted_id)
    }), 201

    

@message_blueprint.route('/messages', methods=['GET'])
@token_required
def get_messages(current_user):
    """
    Listar mensagens do usuário com filtros
    """
    limit = int(request.args.get('limit', 50))
    skip = int(request.args.get('skip', 0))
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    
    messages = message_model.get_user_messages(str(current_user['_id']), limit, skip, unread_only)
    
    # Processar mensagens
    processed_messages = []
    for msg in messages:
        if msg.get('deleted'):
            continue
            
        message_data = {
            '_id': str(msg['_id']),
            'from_user_id': str(msg['from_user_id']),
            'to_user_id': str(msg['to_user_id']),
            'content': msg['content'],
            'type': msg['type'],
            'priority': msg['priority'],
            'timestamp': msg['timestamp'].isoformat(),
            'read': msg['read'],
            'direction': 'outgoing' if str(msg['from_user_id']) == str(current_user['_id']) else 'incoming'
        }
        
        # Adicionar informações do outro usuário
        other_user_id = msg['from_user_id'] if message_data['direction'] == 'incoming' else msg['to_user_id']
        other_user = user_model.find_user_by_id(str(other_user_id))
        if other_user:
            message_data['other_user_name'] = other_user['nome']
            message_data['other_user_type'] = other_user['tipo']
        
        processed_messages.append(message_data)
    
    return jsonify({
        'status': 'sucesso',
        'data': processed_messages,
        'total': len(processed_messages)
    }), 200

@message_blueprint.route('/messages/conversations', methods=['GET'])
@token_required
def get_conversations(current_user):
    """
    Listar todas as conversas do usuário
    """
    # Buscar todas as mensagens para encontrar conversas únicas
    all_messages = message_model.get_user_messages(str(current_user['_id']), limit=1000)
    
    conversations = {}
    for msg in all_messages:
        if msg.get('deleted'):
            continue
            
        # Determinar o ID do outro usuário na conversa
        if str(msg['from_user_id']) == str(current_user['_id']):
            other_user_id = str(msg['to_user_id'])
        else:
            other_user_id = str(msg['from_user_id'])
        
        # Buscar informações do outro usuário
        if other_user_id not in conversations:
            other_user = user_model.find_user_by_id(other_user_id)
            if not other_user:
                continue
                
            unread_count = message_model.get_unread_count(str(current_user['_id']))
            
            conversations[other_user_id] = {
                'user_id': other_user_id,
                'user_name': other_user['nome'],
                'user_type': other_user['tipo'],
                'last_message': msg['content'],
                'last_message_time': msg['timestamp'].isoformat(),
                'unread_count': unread_count,
                'last_message_direction': 'outgoing' if str(msg['from_user_id']) == str(current_user['_id']) else 'incoming'
            }
    
    return jsonify({
        'status': 'sucesso',
        'data': list(conversations.values())
    }), 200

@message_blueprint.route('/messages/<message_id>/read', methods=['PUT'])
@token_required
def mark_message_read(current_user, message_id):
    """
    Marcar mensagem como lida
    """
    result = message_model.mark_as_read(message_id, str(current_user['_id']))
    
    if result.modified_count == 0:
        return jsonify({'status': 'erro', 'message': 'Mensagem não encontrada ou já está lida'}), 404
    
    return jsonify({
        'status': 'sucesso',
        'message': 'Mensagem marcada como lida'
    }), 200

@message_blueprint.route('/messages/conversation/<other_user_id>/read', methods=['PUT'])
@token_required
def mark_conversation_read(current_user, other_user_id):
    """
    Marcar toda uma conversa como lida
    """
    result = message_model.mark_conversation_read(str(current_user['_id']), other_user_id)
    
    return jsonify({
        'status': 'sucesso',
        'message': f'{result.modified_count} mensagens marcadas como lidas'
    }), 200

@message_blueprint.route('/messages/unread/count', methods=['GET'])
@token_required
def get_unread_count(current_user):
    """
    Contar mensagens não lidas
    """
    count = message_model.get_unread_count(str(current_user['_id']))
    
    return jsonify({
        'status': 'sucesso',
        'count': count
    }), 200

@message_blueprint.route('/messages/<message_id>', methods=['DELETE'])
@token_required
def delete_message(current_user, message_id):
    """
    Deletar mensagem (arquivamento)
    """
    result = message_model.delete_message(message_id, str(current_user['_id']))
    
    if result.modified_count == 0:
        return jsonify({'status': 'erro', 'message': 'Mensagem não encontrada'}), 404
    
    return jsonify({
        'status': 'sucesso',
        'message': 'Mensagem deletada'
    }), 200