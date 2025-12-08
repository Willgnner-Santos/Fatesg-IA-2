# app/Models/challenge_model.py
from app import mongo
from bson.objectid import ObjectId
import datetime

class ChallengeModel:
    def create_challenge(self, challenge_data):
        """Cria um novo desafio (função para administradores/professores no futuro)."""
        return mongo.db.challenges.insert_one({
            "title": challenge_data['title'],
            "description": challenge_data['description'],
            "points": challenge_data.get('points', 10),
            "start_date": datetime.datetime.utcnow(),
            "end_date": challenge_data.get('end_date'), # Data limite para o desafio
            "is_active": True,
            "created_by": ObjectId(challenge_data['created_by'])
        })

    def get_active_challenges(self):
        """Busca todos os desafios que estão atualmente ativos."""
        return list(mongo.db.challenges.find({
            "is_active": True,
            # Poderíamos adicionar um filtro de data aqui no futuro
        }).sort("start_date", -1))

    def complete_challenge(self, aluno_id, challenge_id):
        """Regista que um aluno completou um desafio."""
        # Verifica se o aluno já completou este desafio para evitar duplicados
        existing_completion = mongo.db.challenge_completions.find_one({
            "aluno_id": ObjectId(aluno_id),
            "challenge_id": ObjectId(challenge_id)
        })
        if existing_completion:
            return None # Retorna None para indicar que já foi completado

        return mongo.db.challenge_completions.insert_one({
            "aluno_id": ObjectId(aluno_id),
            "challenge_id": ObjectId(challenge_id),
            "completed_at": datetime.datetime.utcnow()
        })

    def get_student_completions(self, aluno_id):
        """Busca todos os desafios que um aluno já completou."""
        return list(mongo.db.challenge_completions.find({
            "aluno_id": ObjectId(aluno_id)
        }))

    def get_challenge_by_id(self, challenge_id):
        """Busca um desafio específico pelo seu ID."""
        return mongo.db.challenges.find_one({"_id": ObjectId(challenge_id)})

    def update_challenge(self, challenge_id, update_data):
        """Atualiza um desafio existente."""
        # remover campos não permitidos
        update_data.pop('_id', None)
        return mongo.db.challenges.update_one({"_id": ObjectId(challenge_id)}, {"$set": update_data})

    def delete_challenge(self, challenge_id):
        """Remove um desafio (soft delete ou hard delete)."""
        # Por enquanto, realizamos hard delete
        return mongo.db.challenges.delete_one({"_id": ObjectId(challenge_id)})