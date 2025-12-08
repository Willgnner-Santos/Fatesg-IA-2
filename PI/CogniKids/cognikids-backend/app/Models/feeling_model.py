from app import mongo
from bson.objectid import ObjectId
import datetime

class Feeling:
    def create_feeling(self, feeling_data):
        """
        Cria um novo registro de sentimento na base de dados.
        """
        return mongo.db.feelings.insert_one({
            "aluno_id": ObjectId(feeling_data['aluno_id']),
            "sentimento": feeling_data['sentimento'], # Ex: "feliz", "triste"
            "emoji": feeling_data['emoji'],           # Ex: "😊", "😢"
            "descricao": feeling_data.get('descricao', ''), # Opcional
            "timestamp": datetime.datetime.utcnow()
        })

    def find_feelings_by_aluno_id(self, aluno_id):
        """
        Encontra todos os registos de sentimento de um aluno específico.
        """
        return list(mongo.db.feelings.find({"aluno_id": ObjectId(aluno_id)}))
    
    def find_all_feelings(self):
        """
        Encontra todos os registos de sentimento na base de dados.
        """
        # O .sort("_id", -1) retorna os registos mais recentes primeiro.
        return list(mongo.db.feelings.find().sort("_id", -1))
    
    def find_feelings_by_aluno_ids(self, aluno_ids_list):
        """
        Encontra todos os registos de sentimento para uma lista de IDs de alunos.
        """
        # Converte a lista de strings de IDs para uma lista de ObjectIds
        object_id_list = [ObjectId(aluno_id) for aluno_id in aluno_ids_list]
        return list(mongo.db.feelings.find({
            "aluno_id": {"$in": object_id_list}
        }).sort("_id", -1))