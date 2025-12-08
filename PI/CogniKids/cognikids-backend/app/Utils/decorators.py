from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.Models.user_model import User

user_model = User()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            logger.info(f"Authorization header recebido: {auth_header[:40]}...")
            parts = auth_header.split(" ")
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
            else:
                token = auth_header  # fallback para token puro

        if not token:
            logger.warning("Token em falta no header Authorization!")
            return jsonify({'status': 'erro', 'message': 'Token em falta!'}), 401

        try:
            logger.info(f"Token recebido para validaÃ§Ã£o: {token[:30]}... (tamanho: {len(token)})")
            logger.info(f"SECRET_KEY usada para validaÃ§Ã£o: {str(current_app.config['SECRET_KEY'])[:10]}...")
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            logger.info(f"Token decodificado com sucesso: {data}")
            current_user = user_model.find_user_by_id(data['user_id'])
            if current_user is None:
                logger.warning("Usuário não encontrado para user_id extraído do token!")
                return jsonify({'status': 'erro', 'message': 'Token inválido! (Utilizador não encontrado)'}), 401
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado!")
            return jsonify({'status': 'erro', 'message': 'Token expirado!'}), 401
        except Exception as e:
            logger.error(f"Erro ao descodificar o token: {e}")
            logger.error(f"Tipo do erro: {type(e).__name__}")
            return jsonify({'status': 'erro', 'message': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated