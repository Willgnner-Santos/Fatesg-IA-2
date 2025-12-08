from app import mongo
from bson.objectid import ObjectId
import datetime

class Schedule:
    def create_event(self, event_data):
        """
        Cria um novo evento na agenda
        """
        return mongo.db.events.insert_one({
            "title": event_data['title'],
            "description": event_data.get('description', ''),
            "type": event_data['type'],  # aula, prova, evento, reuniao, feriado
            "class_id": ObjectId(event_data['class_id']) if event_data.get('class_id') else None,
            "subject": event_data.get('subject', ''),
            "start_date": event_data['start_date'],
            "end_date": event_data['end_date'],
            "all_day": event_data.get('all_day', False),
            "location": event_data.get('location', ''),
            "created_by": ObjectId(event_data['created_by']),
            "participants": event_data.get('participants', []),  # IDs de usuários
            "reminder": event_data.get('reminder'),  # Tempo para lembrete
            "color": event_data.get('color', '#3B82F6'),  # Cor do evento
            "created_at": datetime.datetime.utcnow(),
            "is_active": True
        })
    
    def get_events(self, filters=None):
        """
        Busca eventos com filtros
        """
        query = {"is_active": True}
        if filters:
            query.update(filters)
            
        return list(mongo.db.events.find(query).sort("start_date", 1))
    
    def get_event_by_id(self, event_id):
        """
        Busca um evento por ID
        """
        return mongo.db.events.find_one({"_id": ObjectId(event_id), "is_active": True})
    
    def get_class_events(self, class_id, start_date=None, end_date=None):
        """
        Busca eventos de uma turma específica
        """
        query = {
            "class_id": ObjectId(class_id),
            "is_active": True
        }
        
        if start_date and end_date:
            query["start_date"] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            query["start_date"] = {"$gte": start_date}
        elif end_date:
            query["start_date"] = {"$lte": end_date}
            
        return list(mongo.db.events.find(query).sort("start_date", 1))
    
    def get_user_events(self, user_id, start_date=None, end_date=None):
        """
        Busca eventos de um usuário (baseado em turmas e participantes)
        """
        # Primeiro, buscar turmas do usuário
        from app.Models.class_model import Class
        class_model = Class()
        
        user_classes = []
        if user_id:
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                if user['tipo'] == 'aluno':
                    user_classes = class_model.get_student_classes(user_id)
                elif user['tipo'] == 'professor':
                    user_classes = class_model.get_teacher_classes(user_id)
        
        class_ids = [ObjectId(cls['_id']) for cls in user_classes] if user_classes else []
        
        query = {
            "$or": [
                {"class_id": {"$in": class_ids}},
                {"participants": ObjectId(user_id)},
                {"created_by": ObjectId(user_id)}
            ],
            "is_active": True
        }
        
        if start_date and end_date:
            query["start_date"] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            query["start_date"] = {"$gte": start_date}
        elif end_date:
            query["start_date"] = {"$lte": end_date}
            
        return list(mongo.db.events.find(query).sort("start_date", 1))
    
    def update_event(self, event_id, update_data):
        """
        Atualiza um evento
        """
        return mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_data}
        )
    
    def delete_event(self, event_id):
        """
        Exclui um evento (soft delete)
        """
        return mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": {"is_active": False}}
        )
    
    def add_participant(self, event_id, user_id):
        """
        Adiciona participante a um evento
        """
        return mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$addToSet": {"participants": ObjectId(user_id)}}
        )
    
    def remove_participant(self, event_id, user_id):
        """
        Remove participante de um evento
        """
        return mongo.db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$pull": {"participants": ObjectId(user_id)}}
        )
    
    def get_upcoming_events(self, user_id, days=7):
        """
        Busca eventos próximos para um usuário
        """
        today = datetime.datetime.utcnow()
        end_date = today + datetime.timedelta(days=days)
        
        events = self.get_user_events(user_id, today, end_date)
        return events