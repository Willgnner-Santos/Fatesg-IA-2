from flask import request, jsonify, Blueprint
from app.Utils.decorators import token_required
from app.Models.schedule_model import Schedule
from app.Models.class_model import Class
from app.Models.user_model import User
from bson.objectid import ObjectId

schedule_blueprint = Blueprint('schedule', __name__)
schedule_model = Schedule()
class_model = Class()
user_model = User()

@schedule_blueprint.route('/events', methods=['POST'])
@token_required
def create_event(current_user):
    """
    Criar um novo evento na agenda
    ---
    tags:
      - Agenda Escolar
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
            - start_date
            - end_date
          properties:
            title:
              type: string
              example: "Prova de Matemática"
            type:
              type: string
              enum: ["aula", "prova", "evento", "reuniao", "feriado", "trabalho"]
              example: "prova"
            class_id:
              type: string
              example: "507f1f77bcf86cd799439012"
            subject:
              type: string
              example: "Matemática"
            description:
              type: string
              example: "Prova do capítulo 5"
            start_date:
              type: string
              format: date-time
              example: "2024-02-15T08:00:00Z"
            end_date:
              type: string
              format: date-time
              example: "2024-02-15T09:30:00Z"
    responses:
      201:
        description: Evento criado com sucesso
      400:
        description: Dados em falta
      403:
        description: Acesso não autorizado
    """
    if current_user['tipo'] not in ['professor', 'admin']: # Apenas professores ou admins podem criar eventos
        return jsonify({'status': 'erro', 'message': 'Acesso não autorizado para criar eventos'}), 403

    data = request.get_json()
    required_fields = ['title', 'type', 'start_date', 'end_date']
    
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'erro', 'message': 'Campos obrigatórios em falta'}), 400

    if data.get('class_id'):
        class_data = class_model.get_class_by_id(data['class_id'])
        if not class_data:
            return jsonify({'status': 'erro', 'message': 'Turma não encontrada'}), 404
        if current_user['tipo'] == 'professor' and str(class_data['teacher_id']) != str(current_user['_id']):
            return jsonify({'status': 'erro', 'message': 'Acesso não autorizado a esta turma'}), 403

    event_data = {
        'title': data['title'], 'type': data['type'], 'start_date': data['start_date'],
        'end_date': data['end_date'], 'class_id': data.get('class_id'),
        'subject': data.get('subject', ''), 'description': data.get('description', ''),
        'all_day': data.get('all_day', False), 'location': data.get('location', ''),
        'created_by': str(current_user['_id']), 'participants': data.get('participants', []),
        'reminder': data.get('reminder'), 'color': data.get('color', '#3B82F6')
    }
    
    result = schedule_model.create_event(event_data)
    
    return jsonify({
        'status': 'sucesso',
        'message': 'Evento criado com sucesso!',
        'event_id': str(result.inserted_id)
    }), 201

@schedule_blueprint.route('/events', methods=['GET'])
@token_required
def get_events(current_user):
    """
    Listar eventos do usuário
    ---
    tags:
      - Agenda Escolar
    security:
      - BearerAuth: []
    parameters:
      - in: query
        name: start_date
        schema:
          type: string
          format: date-time
        description: Data de início para filtrar eventos
      - in: query
        name: end_date
        schema:
          type: string
          format: date-time
        description: Data de fim para filtrar eventos
      - in: query
        name: class_id
        schema:
          type: string
        description: Filtrar por turma específica
    responses:
      200:
        description: Lista de eventos
      500:
        description: Erro interno no servidor
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        class_id = request.args.get('class_id')
        
        user_id_str = str(current_user['_id'])
        user_type = current_user['tipo']
        
        query_filter = {}
        
        # --- LÓGICA DE PERMISSÃO ATUALIZADA ---
        if user_type == 'professor':
            # Professor vê eventos que criou ou de suas turmas
            teacher_classes = class_model.get_classes_by_teacher(user_id_str)
            teacher_class_ids = [str(c['_id']) for c in teacher_classes]
            query_filter['$or'] = [
                {'created_by': user_id_str},
                {'class_id': {'$in': teacher_class_ids}}
            ]
        elif user_type == 'aluno':
            # Aluno vê eventos de suas turmas
            student_classes = class_model.get_student_classes(user_id_str)
            student_class_ids = [str(c['_id']) for c in student_classes]
            query_filter['class_id'] = {'$in': student_class_ids}
        elif user_type == 'Responsavel':
            # Responsável vê eventos das turmas dos seus filhos
            children_ids = current_user.get('alunos_ids', [])
            children_class_ids = set()
            for child_id in children_ids:
                child_classes = class_model.get_student_classes(str(child_id))
                for c in child_classes:
                    children_class_ids.add(str(c['_id']))
            query_filter['class_id'] = {'$in': list(children_class_ids)}
        
        if class_id: # Se um class_id específico for solicitado, ele sobrepõe o filtro geral
            query_filter['class_id'] = class_id

        events = schedule_model.get_events_by_filter(query_filter, start_date, end_date)
        
        processed_events = []
        for event in events:
            processed_event = {
                '_id': str(event['_id']), 'title': event['title'], 'type': event['type'],
                'start_date': event['start_date'], 'end_date': event['end_date'],
                'class_id': str(event.get('class_id')), 'location': event.get('location', ''),
                'color': event.get('color', '#3B82F6'), 'created_by': str(event.get('created_by'))
            }
            processed_events.append(processed_event)
        
        return jsonify({'status': 'sucesso', 'data': processed_events}), 200
        
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@schedule_blueprint.route('/events/<event_id>', methods=['GET'])
@token_required
def get_event(current_user, event_id):
    """
    Obter detalhes de um evento específico
    ---
    tags:
      - Agenda Escolar
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: event_id
        required: true
        schema:
          type: string
    responses:
      200:
        description: Detalhes do evento
      403:
        description: Acesso não autorizado
      404:
        description: Evento não encontrado
    """
    try:
        event = schedule_model.get_event_by_id(event_id)
        if not event:
            return jsonify({'status': 'erro', 'message': 'Evento não encontrado'}), 404
        
        # --- LÓGICA DE PERMISSÃO ATUALIZADA ---
        has_access = False
        user_id_str = str(current_user['_id'])
        user_type = current_user['tipo']
        event_class_id = str(event.get('class_id'))

        if str(event.get('created_by')) == user_id_str:
            has_access = True
        
        if not has_access and event_class_id:
            if user_type == 'professor':
                teacher_classes = class_model.get_classes_by_teacher(user_id_str)
                if event_class_id in [str(c['_id']) for c in teacher_classes]:
                    has_access = True
            elif user_type == 'aluno':
                student_classes = class_model.get_student_classes(user_id_str)
                if event_class_id in [str(c['_id']) for c in student_classes]:
                    has_access = True
            elif user_type == 'Responsavel':
                children_ids = current_user.get('alunos_ids', [])
                for child_id in children_ids:
                    child_classes = class_model.get_student_classes(str(child_id))
                    if event_class_id in [str(c['_id']) for c in child_classes]:
                        has_access = True
                        break
        
        if not has_access:
            return jsonify({'status': 'erro', 'message': 'Acesso não autorizado a este evento'}), 403
        
        response_data = {
            '_id': str(event['_id']), 'title': event['title'], 'type': event['type'],
            'class_id': event_class_id, 'subject': event.get('subject', ''),
            'description': event.get('description', ''), 'start_date': event['start_date'],
            'end_date': event['end_date'], 'all_day': event.get('all_day', False),
            'location': event.get('location', ''), 'color': event.get('color', '#3B82F6'),
            'created_by': str(event.get('created_by')), 'participants': [str(p) for p in event.get('participants', [])],
            'reminder': event.get('reminder'), 'created_at': event['created_at'].isoformat()
        }
        
        return jsonify({'status': 'sucesso', 'data': response_data}), 200
        
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@schedule_blueprint.route('/events/<event_id>', methods=['PUT'])
@token_required
def update_event(current_user, event_id):
    """
    Atualizar um evento
    ---
    tags:
      - Agenda Escolar
    security:
      - BearerAuth: []
    # ... (o resto da documentação do Swagger permanece o mesmo)
    """
    try:
        event = schedule_model.get_event_by_id(event_id)
        if not event:
            return jsonify({'status': 'erro', 'message': 'Evento não encontrado'}), 404
        
        if str(event.get('created_by')) != str(current_user['_id']):
            return jsonify({'status': 'erro', 'message': 'Apenas o criador pode editar o evento'}), 403
        
        data = request.get_json()
        update_data = {key: data[key] for key in ['title', 'description', 'start_date', 'end_date', 'location', 'color', 'all_day', 'reminder', 'subject'] if key in data}
        
        result = schedule_model.update_event(event_id, update_data)
        
        if result.modified_count == 0:
            return jsonify({'status': 'informacao', 'message': 'Nenhuma alteração foi feita'}), 200
        
        return jsonify({'status': 'sucesso', 'message': 'Evento atualizado com sucesso!'}), 200
        
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500

@schedule_blueprint.route('/events/<event_id>', methods=['DELETE'])
@token_required
def delete_event(current_user, event_id):
    """
    Excluir um evento
    ---
    tags:
      - Agenda Escolar
    security:
      - BearerAuth: []
    # ... (o resto da documentação do Swagger permanece o mesmo)
    """
    try:
        event = schedule_model.get_event_by_id(event_id)
        if not event:
            return jsonify({'status': 'erro', 'message': 'Evento não encontrado'}), 404
        
        if str(event.get('created_by')) != str(current_user['_id']):
            return jsonify({'status': 'erro', 'message': 'Apenas o criador pode excluir o evento'}), 403
        
        schedule_model.delete_event(event_id)
        
        return jsonify({'status': 'sucesso', 'message': 'Evento excluído com sucesso!'}), 200
        
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500