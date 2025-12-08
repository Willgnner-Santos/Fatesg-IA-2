# app/Models/qa_model.py
from app import mongo
from bson.objectid import ObjectId
import datetime

class QAModel:
    def ask_question(self, question_data):
        """Salva uma nova pergunta no banco de dados."""
        return mongo.db.questions.insert_one({
            "aluno_id": ObjectId(question_data['aluno_id']),
            "class_id": ObjectId(question_data['class_id']),
            "professor_id": ObjectId(question_data['professor_id']),
            "question_text": question_data['question_text'],
            "answer_text": None,
            "asked_at": datetime.datetime.utcnow(),
            "answered_at": None,
            "status": "asked"  # Status pode ser: asked, answered
        })

    def answer_question(self, question_id, answer_text, professor_id):
        """Salva a resposta de um professor a uma pergunta."""
        return mongo.db.questions.update_one(
            {
                "_id": ObjectId(question_id),
                "professor_id": ObjectId(professor_id) # Garante que apenas o professor certo responda
            },
            {
                "$set": {
                    "answer_text": answer_text,
                    "answered_at": datetime.datetime.utcnow(),
                    "status": "answered"
                }
            }
        )

    def get_questions_for_professor(self, professor_id):
        """Busca todas as perguntas direcionadas a um professor."""
        return list(mongo.db.questions.find({
            "professor_id": ObjectId(professor_id)
        }).sort("asked_at", -1))

    def get_questions_from_student(self, aluno_id, class_id=None):
        """Busca todas as perguntas feitas por um aluno específico."""
        query = {"aluno_id": ObjectId(aluno_id)}
        if class_id:
            query["class_id"] = ObjectId(class_id)
        
        return list(mongo.db.questions.find(query).sort("asked_at", -1))
        
    def get_question_by_id(self, question_id):
        """Busca uma pergunta específica pelo seu ID."""
        return mongo.db.questions.find_one({"_id": ObjectId(question_id)})