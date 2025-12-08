from app import mongo
from bson.objectid import ObjectId
from datetime import datetime

class Report:
    def __init__(self):
        self.collection = mongo.db.reports

    def create_report(self, report_data):
        """Cria um novo registro de relatório."""
        report_data['date'] = report_data.get('date', datetime.utcnow())
        
        if 'teacher_id' in report_data and isinstance(report_data['teacher_id'], str):
            report_data['teacher_id'] = ObjectId(report_data['teacher_id'])
            
        return self.collection.insert_one(report_data)

    def find_by_teacher_id(self, teacher_id):
        """Encontra todos os relatórios de um professor específico."""
        return list(self.collection.find({'teacher_id': ObjectId(teacher_id)}).sort('date', -1))

    def find_by_id(self, report_id):
        """Encontra um relatório pelo seu ID."""
        return self.collection.find_one({'_id': ObjectId(report_id)})
