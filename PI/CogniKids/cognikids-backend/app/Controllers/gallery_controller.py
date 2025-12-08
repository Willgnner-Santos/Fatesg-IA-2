# app/Controllers/gallery_controller.py

from flask import Blueprint, request, jsonify
from app.Utils.decorators import token_required
from app.Models.gallery_model import GalleryModel
from app.Models.class_model import Class
from bson.objectid import ObjectId
import os

# --- Configuração de Upload ---
# É importante ter uma pasta para guardar os uploads.
# Adicione UPLOAD_FOLDER = 'uploads' à configuração da sua app se não existir.
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# -----------------------------

gallery_blueprint = Blueprint('gallery_bp', __name__)
gallery_model = GalleryModel()
class_model = Class()

@gallery_blueprint.route('/gallery/upload', methods=['POST'])
@token_required
def upload_creation(current_user):
    """
    (ALUNO) Faz o upload de uma nova criação.
    O ficheiro deve ser enviado como 'multipart/form-data'.
    """
    if current_user['tipo'] != 'aluno':
        return jsonify({'status': 'erro', 'message': 'Apenas alunos podem enviar criações'}), 403

    # Verifica se os dados do formulário e o ficheiro foram enviados
    if 'file' not in request.files or not request.form.get('class_id') or not request.form.get('title'):
        return jsonify({'status': 'erro', 'message': 'Ficheiro, class_id e title são obrigatórios'}), 400

    file = request.files['file']
    class_id = request.form.get('class_id')
    title = request.form.get('title')
    description = request.form.get('description', '')

    # Verifica se o ficheiro tem um nome
    if file.filename == '':
        return jsonify({'status': 'erro', 'message': 'Nenhum ficheiro selecionado'}), 400

    # Lógica para guardar o ficheiro (exemplo simples)
    # Numa aplicação real, usaria nomes de ficheiro seguros e talvez um serviço como S3
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    file_url = f"/uploads/{file.filename}" # URL para aceder ao ficheiro

    creation_data = {
        'aluno_id': str(current_user['_id']),
        'class_id': class_id,
        'title': title,
        'description': description,
        'file_url': file_url
    }
    
    result = gallery_model.add_creation(creation_data)
    
    return jsonify({
        'status': 'sucesso',
        'message': 'Criação enviada com sucesso! Aguardando aprovação do professor.',
        'creation_id': str(result.inserted_id)
    }), 201


@gallery_blueprint.route('/gallery/class/<string:class_id>', methods=['GET'])
@token_required
def get_class_gallery(current_user, class_id):
    """
    (PROFESSOR/PAI/ALUNO) Obtém todas as criações APROVADAS de uma turma.
    """
    # Lógica de permissão (verificar se o utilizador tem acesso à turma)
    # ... (esta lógica pode ser adicionada aqui) ...

    creations = gallery_model.get_creations_by_class(class_id)
    for c in creations:
        c['_id'] = str(c['_id'])
        c['aluno_id'] = str(c['aluno_id'])
        c['class_id'] = str(c['class_id'])
    
    return jsonify({'status': 'sucesso', 'data': creations}), 200


@gallery_blueprint.route('/gallery/creation/<string:creation_id>/approve', methods=['PUT'])
@token_required
def approve_creation(current_user, creation_id):
    """
    (PROFESSOR) Aprova uma criação para ser exibida na galeria.
    """
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Apenas professores podem aprovar criações'}), 403

    result = gallery_model.approve_creation(creation_id, str(current_user['_id']))

    if result.modified_count == 0:
        return jsonify({'status': 'erro', 'message': 'Criação não encontrada ou já aprovada'}), 404

    return jsonify({'status': 'sucesso', 'message': 'Criação aprovada com sucesso!'}), 200