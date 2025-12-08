# app/Controllers/qa_controller.py

from flask import Blueprint, request, jsonify
from app.Utils.decorators import token_required
from app.Models.qa_model import QAModel
from app.Models.class_model import Class
from app.Models.user_model import User
from bson.objectid import ObjectId

qa_blueprint = Blueprint('qa_bp', __name__)
qa_model = QAModel()
class_model = Class()
user_model = User()

@qa_blueprint.route('/qa/ask', methods=['POST'])
@token_required
def ask_question(current_user):
    """
    (ALUNO) Envia uma pergunta para o professor de uma turma.
    """
    if current_user['tipo'] != 'aluno':
        return jsonify({'status': 'erro', 'message': 'Apenas alunos podem fazer perguntas'}), 403

    data = request.get_json()
    if not data or not data.get('class_id') or not data.get('question_text'):
        return jsonify({'status': 'erro', 'message': 'class_id e question_text são obrigatórios'}), 400

    class_data = class_model.get_class_by_id(data['class_id'])
    if not class_data:
        return jsonify({'status': 'erro', 'message': 'Turma não encontrada'}), 404
        
    # Verifica se o aluno realmente pertence à turma
    if ObjectId(current_user['_id']) not in class_data.get('students', []):
        return jsonify({'status': 'erro', 'message': 'Você não está matriculado nesta turma'}), 403

    question_data = {
        "aluno_id": str(current_user['_id']),
        "class_id": data['class_id'],
        "professor_id": str(class_data['teacher_id']),
        "question_text": data['question_text']
    }
    
    result = qa_model.ask_question(question_data)

    return jsonify({
        'status': 'sucesso',
        'message': 'Pergunta enviada com sucesso!',
        'question_id': str(result.inserted_id)
    }), 201


@qa_blueprint.route('/qa/questions/professor', methods=['GET'])
@token_required
def get_questions_for_professor(current_user):
    """
    (PROFESSOR) Obtém todas as perguntas direcionadas ao professor logado.
    """
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado'}), 403

    questions = qa_model.get_questions_for_professor(str(current_user['_id']))

    for q in questions:
        q['_id'] = str(q['_id'])
        q['aluno_id'] = str(q['aluno_id'])
        q['class_id'] = str(q['class_id'])
        q['professor_id'] = str(q['professor_id'])

    return jsonify({'status': 'sucesso', 'data': questions}), 200


@qa_blueprint.route('/qa/questions/student/<string:student_id>', methods=['GET'])
@token_required
def get_student_questions(current_user, student_id):
    """
    (PAI/ALUNO) Obtém as perguntas de um aluno específico.
    """
    student_id_obj = ObjectId(student_id)
    has_access = False

    if current_user['tipo'] == 'aluno' and str(current_user['_id']) == student_id:
        has_access = True
    elif current_user['tipo'] == 'pai' and student_id_obj in current_user.get('filhos_ids', []):
        has_access = True
    
    if not has_access:
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado para ver as perguntas deste aluno'}), 403

    questions = qa_model.get_questions_from_student(student_id)
    for q in questions:
        q['_id'] = str(q['_id'])
        q['aluno_id'] = str(q['aluno_id'])
        q['class_id'] = str(q['class_id'])
        q['professor_id'] = str(q['professor_id'])

    return jsonify({'status': 'sucesso', 'data': questions}), 200


@qa_blueprint.route('/qa/answer/<string:question_id>', methods=['PUT'])
@token_required
def answer_question(current_user, question_id):
    """
    (PROFESSOR) Responde a uma pergunta.
    """
    if current_user['tipo'] != 'professor':
        return jsonify({'status': 'erro', 'message': 'Apenas professores podem responder perguntas'}), 403
        
    data = request.get_json()
    if not data or not data.get('answer_text'):
        return jsonify({'status': 'erro', 'message': 'O texto da resposta é obrigatório'}), 400

    result = qa_model.answer_question(question_id, data['answer_text'], str(current_user['_id']))
    
    if result.modified_count == 0:
        return jsonify({'status': 'erro', 'message': 'Pergunta não encontrada ou você não tem permissão para responder'}), 404

    return jsonify({'status': 'sucesso', 'message': 'Pergunta respondida com sucesso!'}), 200