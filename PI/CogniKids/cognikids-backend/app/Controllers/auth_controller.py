from flask import request, jsonify, Blueprint, current_app
from app import bcrypt
from app.Models.user_model import User
from app.Utils.decorators import token_required
import jwt
import datetime
import time
import logging

# Configuracao de logging para monitoramento de performance
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint de autenticacao
auth_blueprint = Blueprint('auth', __name__)
user_model = User()


@auth_blueprint.route('/register', methods=['POST'])
def register():
    start_time = time.time()
    logger.info("Iniciando processo de registro de usuário")
    
    data = request.get_json()
    
    # Extracao segura de dados utilizando .get() para evitar KeyError
    nome = data.get('nome') if data else None
    email = data.get('email') if data else None
    senha = data.get('senha') if data else None
    tipo = data.get('tipo') if data else None
    
    # Validação de campos obrigatórios
    if not all([nome, email, senha, tipo]):
        logger.warning(f"Campos obrigatórios faltando para email: {email}")
        return jsonify({
            'status': 'erro', 
            'message': 'Faltam campos essenciais: nome, email, senha ou tipo (role).'
        }), 400

    # Validação de tipos de usuário permitidos
    tipos_permitidos = ['estudante', 'professor', 'pai', 'admin']
    if tipo not in tipos_permitidos:
        logger.warning(f"Tipo de usuário inválido: {tipo} para email: {email}")
        return jsonify({
            'status': 'erro', 
            'message': f'Tipo de usuário inválido. Tipos permitidos: {", ".join(tipos_permitidos)}'
        }), 400

    # Verificar se usuário já existe
    logger.info(f"Verificando se usuário existe: {email}")
    check_start = time.time()
    if user_model.find_user_by_email(email):
        logger.warning(f"Email já registrado: {email}")
        return jsonify({'status': 'erro', 'message': 'Email já registado'}), 409
    logger.info(f"Verificacao de usuario existente levou: {time.time() - check_start:.3f}s")

    # Geracao do hash da senha no Controller
    try:
        logger.info("Iniciando hash da senha")
        hash_start = time.time()
        hashed_password = bcrypt.generate_password_hash(senha).decode('utf-8')
        logger.info(f"Hash da senha levou: {time.time() - hash_start:.3f}s")
    except Exception as e:
        logger.error(f"Erro no hashing da senha: {str(e)}")
        return jsonify({
            "status": "erro", 
            "message": "Erro de inicializacao de seguranca (Bcrypt). Servidor nao esta pronto."
        }), 500

    # Preparacao dos dados do usuario com senha ja hasheada
    user_data = {
        'nome': nome,
        'email': email,
        'senha': hashed_password,
        'tipo': tipo
    }

    # Persistencia no banco de dados
    logger.info(f"Iniciando criacao do usuario no banco: {email}")
    db_start = time.time()
    result = user_model.create_user(user_data)
    logger.info(f"Operacao de banco levou: {time.time() - db_start:.3f}s")
    
    total_time = time.time() - start_time
    logger.info(f"Processo completo de registro levou: {total_time:.3f}s")
    
    if result.get('success'):
        return jsonify({
            'status': 'sucesso', 
            'message': 'Utilizador registado com sucesso!', 
            'user_id': result.get('user_id')
        }), 201
    else:
        logger.error(f"Erro na criação do usuário: {result.get('message')}")
        # Retorna erro 500 com detalhes do problema de persistência
        return jsonify({
            'status': 'erro', 
            'message': result.get('message', 'Erro interno do servidor'),
            'error': result.get('error')
        }), 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    start_time = time.time()
    logger.info("Iniciando processo de login de usuário")
    
    data = request.get_json()
    
    # Extracao segura de dados utilizando .get() para evitar KeyError
    email = data.get('email') if data else None
    senha = data.get('senha') if data else None
    
    # Validação de campos obrigatórios
    if not all([email, senha]):
        logger.warning(f"Campos obrigatórios faltando para login: {email}")
        return jsonify({
            'status': 'erro', 
            'message': 'Dados em falta: email e senha são obrigatórios.'
        }), 400

    logger.info(f"Tentativa de login para email: {email}")
    user = user_model.find_user_by_email(email)
    if not user:
        logger.warning(f"Usuário não encontrado: {email}")
        return jsonify({'status': 'erro', 'message': 'Email ou senha inválidos'}), 401
    
    # Verificar senha usando bcrypt no controller
    try:
        password_valid = bcrypt.check_password_hash(user['senha'], senha)
    except Exception as e:
        logger.error(f"Erro de verificação de senha: {str(e)}")
        return jsonify({'status': 'erro', 'message': 'Erro de verificação de senha'}), 500
    
    if not password_valid:
        logger.warning(f"Senha incorreta para email: {email}")
        return jsonify({'status': 'erro', 'message': 'Email ou senha inválidos'}), 401

    # Gerar token JWT com informações do usuário
    token_payload = {
        'user_id': str(user['_id']),
        'email': user['email'],
        'role': user['tipo'],  # Incluir role no token
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    
    token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    
    login_time = time.time() - start_time
    logger.info(f"Login bem-sucedido para {email} em {login_time:.3f}s")

    # Mapeamento de roles portugues para ingles
    role_mapping = {
        'professor': 'teacher',
        'pai': 'parent', 
        'estudante': 'student'
    }

    # Resposta com dados do usuario e role
    return jsonify({
        'success': True,
        'status': 'sucesso', 
        'message': 'Login realizado com sucesso!',
        'token': token,
        'role': user['tipo'],  # Enviar role diretamente
        'frontend_role': role_mapping.get(user['tipo'], user['tipo']),  # Role convertido
        'user': {
            'id': str(user['_id']),
            'name': user['nome'],
            'email': user['email'],
            'role': user['tipo'],
            'frontend_role': role_mapping.get(user['tipo'], user['tipo'])
        }
    }), 200

@auth_blueprint.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    user_data = {
        "id": str(current_user["_id"]),
        "nome": current_user["nome"],
        "email": current_user["email"],
        "tipo": current_user["tipo"]
    }
    return jsonify({"status": "sucesso", "user": user_data}), 200