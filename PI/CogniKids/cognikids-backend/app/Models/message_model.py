from app import mongo
from bson.objectid import ObjectId
import datetime

class Message:
    def create_message(self, from_user_id, to_user_id, content, message_type="text", priority="normal"):
        """
        Criar nova mensagem com mais metadados
        """
        return mongo.db.messages.insert_one({
            "from_user_id": ObjectId(from_user_id),
            "to_user_id": ObjectId(to_user_id),
            "content": content,
            "type": message_type,  # text, alert, announcement, urgent
            "priority": priority,  # normal, high, urgent
            "timestamp": datetime.datetime.utcnow(),
            "read": False,
            "related_to": None,  # Pode ser ID de atividade, evento, etc.
            "attachments": []    # Para futuros anexos
        })
    
    def get_user_messages(self, user_id, limit=50, skip=0, unread_only=False):
        """
        Buscar mensagens com filtros
        """
        query = {
            "$or": [
                {"from_user_id": ObjectId(user_id)},
                {"to_user_id": ObjectId(user_id)}
            ]
        }
        
        if unread_only:
            query["read"] = False
        
        return list(mongo.db.messages.find(query)
                         .sort("timestamp", -1)
                         .limit(limit)
                         .skip(skip))
    
    def get_conversation(self, user1_id, user2_id, limit=50):
        """
        Buscar conversa entre dois usuários
        """
        return list(mongo.db.messages.find({
            "$or": [
                {
                    "from_user_id": ObjectId(user1_id),
                    "to_user_id": ObjectId(user2_id)
                },
                {
                    "from_user_id": ObjectId(user2_id), 
                    "to_user_id": ObjectId(user1_id)
                }
            ]
        }).sort("timestamp", -1).limit(limit))
    
    def mark_as_read(self, message_id, user_id):
        """
        Marcar mensagem como lida
        """
        return mongo.db.messages.update_one(
            {
                "_id": ObjectId(message_id),
                "to_user_id": ObjectId(user_id)
            },
            {"$set": {"read": True}}
        )
    
    def mark_conversation_read(self, user1_id, user2_id):
        """
        Marcar todas as mensagens de uma conversa como lidas
        """
        return mongo.db.messages.update_many(
            {
                "to_user_id": ObjectId(user1_id),
                "from_user_id": ObjectId(user2_id),
                "read": False
            },
            {"$set": {"read": True}}
        )
    
    def get_unread_count(self, user_id):
        """
        Contar mensagens não lidas
        """
        return mongo.db.messages.count_documents({
            "to_user_id": ObjectId(user_id),
            "read": False
        })
    
    def delete_message(self, message_id, user_id):
        """
        Deletar mensagem (apenas para o usuário)
        """
        return mongo.db.messages.update_one(
            {
                "_id": ObjectId(message_id),
                "$or": [
                    {"from_user_id": ObjectId(user_id)},
                    {"to_user_id": ObjectId(user_id)}
                ]
            },
            {"$set": {"deleted": True}}
        )