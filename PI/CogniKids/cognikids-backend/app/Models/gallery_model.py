# app/Models/gallery_model.py
from app import mongo
from bson.objectid import ObjectId
import datetime

class GalleryModel:
    def add_creation(self, creation_data):
        """Adiciona uma nova criação de um aluno à galeria."""
        return mongo.db.gallery_creations.insert_one({
            "aluno_id": ObjectId(creation_data['aluno_id']),
            "class_id": ObjectId(creation_data['class_id']),
            "title": creation_data['title'],
            "description": creation_data.get('description', ''),
            "file_url": creation_data['file_url'],  # URL para o ficheiro (upload será tratado no controller)
            "creation_type": creation_data.get('creation_type', 'image'), # pode ser 'image', 'text', 'video'
            "created_at": datetime.datetime.utcnow(),
            "is_approved": False  # Pode ser útil ter um sistema de aprovação por parte dos professores
        })

    def get_creations_by_student(self, aluno_id):
        """Busca todas as criações de um aluno específico."""
        return list(mongo.db.gallery_creations.find({
            "aluno_id": ObjectId(aluno_id)
        }).sort("created_at", -1))

    def get_creations_by_class(self, class_id):
        """Busca todas as criações de uma turma (aprovadas)."""
        return list(mongo.db.gallery_creations.find({
            "class_id": ObjectId(class_id),
            "is_approved": True
        }).sort("created_at", -1))

    def approve_creation(self, creation_id, professor_id):
        """Permite que um professor aprove uma criação para ser exibida."""
        return mongo.db.gallery_creations.update_one(
            {"_id": ObjectId(creation_id)},
            {
                "$set": {
                    "is_approved": True,
                    "approved_by": ObjectId(professor_id),
                    "approved_at": datetime.datetime.utcnow()
                }
            }
        )

    def delete_creation(self, creation_id):
        """Remove uma criação."""
        return mongo.db.gallery_creations.delete_one({"_id": ObjectId(creation_id)})