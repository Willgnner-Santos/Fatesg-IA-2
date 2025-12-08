from flask_pymongo import PyMongo
from flask import current_app
from bson.objectid import ObjectId
from datetime import datetime

class ForumModel:
    def __init__(self):
        pass
    
    @property
    def mongo(self):
        """Acesso ao MongoDB através do Flask-PyMongo"""
        return current_app.extensions['pymongo']
    
    def get_all_topics(self):
        """Obter todos os tópicos do fórum"""
        try:
            return list(self.mongo.db.forum_topics.find().sort('created_at', -1))
        except Exception as e:
            print(f"Erro ao buscar tópicos: {e}")
            return []
    
    def create_topic(self, title, content, author_id, category=None):
        """Criar um novo tópico no fórum"""
        try:
            topic = {
                'title': title,
                'content': content,
                'author_id': ObjectId(author_id),
                'category': category,
                'replies': [],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'is_active': True
            }
            result = self.mongo.db.forum_topics.insert_one(topic)
            return result.inserted_id
        except Exception as e:
            print(f"Erro ao criar tópico: {e}")
            return None
    
    def get_topic_by_id(self, topic_id):
        """Obter tópico por ID"""
        try:
            return self.mongo.db.forum_topics.find_one({'_id': ObjectId(topic_id)})
        except Exception as e:
            print(f"Erro ao buscar tópico: {e}")
            return None
    
    def add_reply(self, topic_id, reply_content, author_id):
        """Adicionar resposta a um tópico"""
        try:
            reply = {
                'content': reply_content,
                'author_id': ObjectId(author_id),
                'created_at': datetime.utcnow()
            }
            
            result = self.mongo.db.forum_topics.update_one(
                {'_id': ObjectId(topic_id)},
                {
                    '$push': {'replies': reply},
                    '$set': {'updated_at': datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao adicionar resposta: {e}")
            return False
    
    def update_topic(self, topic_id, updates):
        """Atualizar tópico"""
        try:
            updates['updated_at'] = datetime.utcnow()
            result = self.mongo.db.forum_topics.update_one(
                {'_id': ObjectId(topic_id)},
                {'$set': updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar tópico: {e}")
            return False
    
    def delete_topic(self, topic_id):
        """Excluir tópico (soft delete)"""
        try:
            result = self.mongo.db.forum_topics.update_one(
                {'_id': ObjectId(topic_id)},
                {'$set': {'is_active': False, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao excluir tópico: {e}")
            return False
    
    def get_topics_by_category(self, category):
        """Obter tópicos por categoria"""
        try:
            return list(self.mongo.db.forum_topics.find({
                'category': category,
                'is_active': True
            }).sort('created_at', -1))
        except Exception as e:
            print(f"Erro ao buscar tópicos por categoria: {e}")
            return []
    
    def get_topics_by_author(self, author_id):
        """Obter tópicos por autor"""
        try:
            return list(self.mongo.db.forum_topics.find({
                'author_id': ObjectId(author_id),
                'is_active': True
            }).sort('created_at', -1))
        except Exception as e:
            print(f"Erro ao buscar tópicos por autor: {e}")
            return []