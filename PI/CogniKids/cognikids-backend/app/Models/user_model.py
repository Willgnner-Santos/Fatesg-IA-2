from app import mongo
from bson.objectid import ObjectId
import time
import logging
from pymongo.errors import PyMongoError, ConnectionFailure, ServerSelectionTimeoutError

# Configurar logging para debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nota: A logica de bcrypt foi movida para auth_controller.py

class User:
    def create_user(self, user_data):
        """Cria um novo utilizador na base de dados."""
        try:
            logger.info(f"Iniciando criação de usuário: {user_data.get('email')}")
            start_time = time.time()
            
            # O campo senha ja contem o hash gerado pelo controller
            
            new_user = {
                "nome": user_data['nome'],
                "email": user_data['email'],
                "senha": user_data['senha'],  # Hash recebido do controller
                "tipo": user_data['tipo']
            }
            
            # Inicializa lista de filhos para usuarios do tipo pai
            if user_data['tipo'] == 'pai':
                new_user['filhos_ids'] = []
            
            # Inicializa lista de turmas para usuarios do tipo professor
            if user_data['tipo'] == 'professor':
                new_user['turmas_ids'] = []

            # Teste de conexão antes da operação
            logger.info("Testando conexão com MongoDB")
            mongo.db.command('ping')
            
            logger.info("Inserindo usuário no banco de dados")
            result = mongo.db.users.insert_one(new_user)
            
            operation_time = time.time() - start_time
            logger.info(f"Usuário criado com sucesso em {operation_time:.3f}s: {result.inserted_id}")
            
            return {"success": True, "message": "Usuário criado com sucesso", "user_id": str(result.inserted_id)}
        
        except ServerSelectionTimeoutError as e:
            logger.error(f"Timeout na seleção do servidor MongoDB: {e}")
            return {"success": False, "message": "Timeout na conexão com o banco de dados", "error": str(e)}
        
        except ConnectionFailure as e:
            logger.error(f"Falha na conexão com MongoDB: {e}")
            return {"success": False, "message": "Falha na conexão com o banco de dados", "error": str(e)}
        
        except PyMongoError as e:
            logger.error(f"Erro específico do MongoDB: {e}")
            return {"success": False, "message": f"Erro do MongoDB: {e}", "error": str(e)}
        
        except Exception as e:
            # Captura erros de conexao ou de banco de dados
            logger.error(f"[ERRO] Falha critica no MongoDB: {e}")
            # O backend deve retornar um erro especifico
            return {"success": False, "message": f"Erro de persistencia no MongoDB: {e}", "error": str(e)}

    def find_user_by_email(self, email):
        """Encontra um utilizador pelo seu email."""
        try:
            logger.info(f"Procurando usuário por email: {email}")
            start_time = time.time()
            
            # Teste de conexão rápido
            mongo.db.command('ping')
            
            result = mongo.db.users.find_one({"email": email})
            
            operation_time = time.time() - start_time
            logger.info(f"Busca por email completada em {operation_time:.3f}s")
            
            return result
            
        except ServerSelectionTimeoutError as e:
            logger.error(f"Timeout na busca por email: {e}")
            return None
            
        except Exception as e:
            logger.error(f"Erro na busca por email: {e}")
            return None

    def find_user_by_id(self, user_id):
        """Encontra um utilizador pelo seu ID único."""
        try:
            return mongo.db.users.find_one({"_id": ObjectId(user_id)})
        except Exception as e:
            logger.error(f"Erro na busca por ID: {e}")
            return None
            
    def link_child_to_parent(self, parent_id, child_id):
        """Adiciona o ID de um filho à lista de filhos de um pai."""
        return mongo.db.users.update_one(
            {"_id": ObjectId(parent_id)},
            {"$addToSet": {"filhos_ids": ObjectId(child_id)}}
        )