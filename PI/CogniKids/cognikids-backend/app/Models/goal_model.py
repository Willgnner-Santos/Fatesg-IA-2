from app import mongo
from bson.objectid import ObjectId
from datetime import datetime

class Goal:
    def __init__(self):
        self.collection = mongo.db.goals

    def create_goal(self, goal_data):
        """Cria uma nova meta para um aluno."""
        goal_data['created_at'] = datetime.utcnow()
        goal_data['updated_at'] = datetime.utcnow()
        goal_data['progress'] = goal_data.get('progress', 0)
        goal_data['status'] = goal_data.get('status', 'current')
        
        if 'student_id' in goal_data and isinstance(goal_data['student_id'], str):
            goal_data['student_id'] = ObjectId(goal_data['student_id'])
            
        return self.collection.insert_one(goal_data)

    def find_by_student_id(self, student_id):
        """Encontra todas as metas de um aluno específico."""
        return list(self.collection.find({'student_id': ObjectId(student_id)}))

    def find_by_id(self, goal_id):
        """Encontra uma meta pelo seu ID."""
        return self.collection.find_one({'_id': ObjectId(goal_id)})

    def update_goal(self, goal_id, update_data):
        """Atualiza uma meta."""
        update_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'_id': ObjectId(goal_id)},
            {'$set': update_data}
        )

    def delete_goal(self, goal_id):
        """Deleta uma meta."""
        return self.collection.delete_one({'_id': ObjectId(goal_id)})
