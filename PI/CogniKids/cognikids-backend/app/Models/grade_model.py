from app import mongo
from bson.objectid import ObjectId
import datetime

class Grade:
    def create_assignment(self, assignment_data):
        """
        Cria uma nova avaliação/trabalho
        """
        return mongo.db.assignments.insert_one({
            "title": assignment_data['title'],
            "description": assignment_data.get('description', ''),
            "type": assignment_data['type'],  # prova, trabalho, participacao, etc.
            "class_id": ObjectId(assignment_data['class_id']),
            "subject": assignment_data['subject'],
            "max_score": assignment_data['max_score'],  # Pontuação máxima
            "due_date": assignment_data.get('due_date'),
            "weight": assignment_data.get('weight', 1.0),  # Peso na média
            "created_by": ObjectId(assignment_data['created_by']),
            "created_at": datetime.datetime.utcnow(),
            "is_active": True
        })
    
    def submit_grade(self, grade_data):
        """
        Lança uma nota para um aluno
        """
        return mongo.db.grades.insert_one({
            "assignment_id": ObjectId(grade_data['assignment_id']),
            "student_id": ObjectId(grade_data['student_id']),
            "class_id": ObjectId(grade_data['class_id']),
            "score": grade_data['score'],
            "feedback": grade_data.get('feedback', ''),
            "graded_by": ObjectId(grade_data['graded_by']),
            "graded_at": datetime.datetime.utcnow(),
            "is_absent": grade_data.get('is_absent', False),
            "comments": grade_data.get('comments', '')
        })
    
    def get_assignment_by_id(self, assignment_id):
        """
        Busca uma avaliação por ID
        """
        return mongo.db.assignments.find_one({"_id": ObjectId(assignment_id)})
    
    def get_class_assignments(self, class_id):
        """
        Busca todas as avaliações de uma turma
        """
        return list(mongo.db.assignments.find({
            "class_id": ObjectId(class_id),
            "is_active": True
        }).sort("due_date", 1))
    
    def get_student_grades(self, student_id, class_id=None):
        """
        Busca todas as notas de um aluno
        """
        query = {"student_id": ObjectId(student_id)}
        if class_id:
            query["class_id"] = ObjectId(class_id)
            
        return list(mongo.db.grades.find(query).sort("graded_at", -1))
    
    def get_assignment_grades(self, assignment_id):
        """
        Busca todas as notas de uma avaliação específica
        """
        return list(mongo.db.grades.find({
            "assignment_id": ObjectId(assignment_id)
        }).sort("graded_at", -1))
    
    def update_grade(self, grade_id, update_data):
        """
        Atualiza uma nota
        """
        return mongo.db.grades.update_one(
            {"_id": ObjectId(grade_id)},
            {"$set": update_data}
        )
    
    def calculate_student_average(self, student_id, class_id):
        """
        Calcula a média do aluno em uma turma
        """
        grades = self.get_student_grades(student_id, class_id)
        
        if not grades:
            return None
        
        total_weight = 0
        weighted_sum = 0
        
        for grade in grades:
            # Buscar informação da avaliação para pegar o peso
            assignment = self.get_assignment_by_id(grade['assignment_id'])
            if assignment and assignment.get('weight'):
                weight = assignment['weight']
                total_weight += weight
                weighted_sum += grade['score'] * weight
        
        if total_weight == 0:
            return None
            
        return weighted_sum / total_weight
    
    def get_class_grades_summary(self, class_id):
        """
        Retorna um resumo das notas da turma
        """
        assignments = self.get_class_assignments(class_id)
        summary = []
        
        for assignment in assignments:
            grades = self.get_assignment_grades(str(assignment['_id']))
            assignment_grades = [grade['score'] for grade in grades if not grade.get('is_absent')]
            
            summary.append({
                'assignment_id': str(assignment['_id']),
                'title': assignment['title'],
                'type': assignment['type'],
                'average': sum(assignment_grades) / len(assignment_grades) if assignment_grades else 0,
                'max_score': assignment['max_score'],
                'total_students': len(grades),
                'graded_students': len([g for g in grades if g.get('score') is not None])
            })
        
        return summary