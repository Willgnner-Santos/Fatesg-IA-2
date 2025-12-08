from app import mongo
from bson.objectid import ObjectId
import datetime

class Class:
    def create_class(self, class_data):
        """
        Cria uma nova turma na base de dados
        """
        return mongo.db.turmas.insert_one({
            "name": class_data['name'],
            "grade": class_data['grade'],           # Ex: "3º Ano", "1ª Série"
            "section": class_data['section'],       # Ex: "A", "B", "C"
            "teacher_id": ObjectId(class_data['teacher_id']),
            "school_year": class_data['school_year'], # Ex: "2024"
            "alunos_ids": [],                       # Lista de IDs de alunos
            "subjects": class_data.get('subjects', []), # Lista de matérias
            "created_at": datetime.datetime.utcnow(),
            "schedule": {}                          # Horário das aulas
        })

    def enroll_student(self, class_id, student_id):
        """
        Matricula um aluno em uma turma
        """
        return mongo.db.turmas.update_one(
            {"_id": ObjectId(class_id)},
            {"$addToSet": {"alunos_ids": ObjectId(student_id)}}
        )

    def remove_student(self, class_id, student_id):
        """
        Remove um aluno de uma turma
        """
        return mongo.db.turmas.update_one(
            {"_id": ObjectId(class_id)},
            {"$pull": {"alunos_ids": ObjectId(student_id)}}
        )

    def get_class_by_id(self, class_id):
        """
        Busca uma turma específica pelo seu ID
        """
        return mongo.db.turmas.find_one({"_id": ObjectId(class_id)})

    def add_student_to_class(self, class_id, student_id):
        """
        Adiciona um aluno a uma turma
        """
        mongo.db.turmas.update_one(
            {'_id': ObjectId(class_id)},
            {'$addToSet': {'alunos_ids': ObjectId(student_id)}}
        )

    def get_teacher_classes(self, teacher_id):
        """
        Busca todas as turmas de um professor
        Usa query padronizada apenas com 'teacher_id'
        """
        teacher_id_obj = ObjectId(teacher_id)
        
        # Query simples e padronizada - banco de dados já está limpo
        query = {"teacher_id": teacher_id_obj}
        
        # Busca turmas e ordena por data de criação
        classes = list(mongo.db.turmas.find(query).sort("created_at", -1))
        
        # Filtra apenas turmas ativas
        active_classes = []
        for c in classes:
            is_active = c.get('ativa', True) and c.get('is_active', True)
            if is_active:
                active_classes.append(c)
        
        return active_classes

    def get_student_classes(self, student_id):
        """
        Busca todas as turmas de um aluno
        """
        return list(mongo.db.turmas.find({
            "alunos_ids": ObjectId(student_id),
        }).sort("created_at", -1))

    def get_all_classes(self):
        """
        Busca todas as turmas ativas
        """
        return list(mongo.db.turmas.find().sort("created_at", -1))

    def update_class(self, class_id, update_data):
        """
        Atualiza informações de uma turma
        """
        return mongo.db.turmas.update_one(
            {"_id": ObjectId(class_id)},
            {"$set": update_data}
        )

    def deactivate_class(self, class_id):
        """
        Desativa uma turma (soft delete)
        """
        return mongo.db.turmas.update_one(
            {"_id": ObjectId(class_id)},
            {"$set": {"is_active": False}}
        )

    def get_class_students(self, class_id):
        """
        Busca todos os alunos de uma turma específica
        """
        class_data = mongo.db.turmas.find_one(
            {"_id": ObjectId(class_id)},
            {"alunos_ids": 1}
        )
        return class_data.get('alunos_ids', []) if class_data else []
