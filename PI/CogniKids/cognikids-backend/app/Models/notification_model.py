from app import mongo
from bson.objectid import ObjectId
import datetime

class Notification:
    def create_notification(self, notification_data):
        """
        Cria uma nova notificação
        """
        return mongo.db.notifications.insert_one({
            "title": notification_data['title'],
            "message": notification_data['message'],
            "type": notification_data['type'],  # info, alert, warning, success, event
            "user_id": ObjectId(notification_data['user_id']),
            "related_to": notification_data.get('related_to'),  # ID de evento, mensagem, etc.
            "related_type": notification_data.get('related_type'),  # event, message, grade, etc.
            "priority": notification_data.get('priority', 'medium'),  # low, medium, high, urgent
            "action_url": notification_data.get('action_url'),  # URL para ação
            "action_text": notification_data.get('action_text'),  # Texto do botão de ação
            "read": False,
            "sent": False,
            "scheduled_for": notification_data.get('scheduled_for'),
            "created_at": datetime.datetime.utcnow(),
            "expires_at": notification_data.get('expires_at')
        })
    
    def get_user_notifications(self, user_id, unread_only=False, limit=50, skip=0):
        """
        Busca notificações de um usuário
        """
        query = {"user_id": ObjectId(user_id)}
        
        if unread_only:
            query["read"] = False
            
        return list(mongo.db.notifications.find(query)
                         .sort("created_at", -1)
                         .limit(limit)
                         .skip(skip))
    
    def get_unread_count(self, user_id):
        """
        Conta notificações não lidas de um usuário
        """
        return mongo.db.notifications.count_documents({
            "user_id": ObjectId(user_id),
            "read": False
        })
    
    def mark_as_read(self, notification_id, user_id):
        """
        Marca uma notificação como lida
        """
        return mongo.db.notifications.update_one(
            {
                "_id": ObjectId(notification_id),
                "user_id": ObjectId(user_id)
            },
            {"$set": {"read": True, "read_at": datetime.datetime.utcnow()}}
        )
    
    def mark_all_as_read(self, user_id):
        """
        Marca todas as notificações do usuário como lidas
        """
        return mongo.db.notifications.update_many(
            {
                "user_id": ObjectId(user_id),
                "read": False
            },
            {"$set": {"read": True, "read_at": datetime.datetime.utcnow()}}
        )
    
    def delete_notification(self, notification_id, user_id):
        """
        Exclui uma notificação
        """
        return mongo.db.notifications.delete_one({
            "_id": ObjectId(notification_id),
            "user_id": ObjectId(user_id)
        })
    
    def create_bulk_notifications(self, notifications_data):
        """
        Cria múltiplas notificações de uma vez
        """
        return mongo.db.notifications.insert_many(notifications_data)
    
    def get_recent_notifications(self, user_id, hours=24):
        """
        Busca notificações recentes (últimas X horas)
        """
        time_threshold = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
        
        return list(mongo.db.notifications.find({
            "user_id": ObjectId(user_id),
            "created_at": {"$gte": time_threshold}
        }).sort("created_at", -1))
    
    def schedule_notification(self, notification_data):
        """
        Agenda uma notificação para o futuro
        """
        return self.create_notification(notification_data)