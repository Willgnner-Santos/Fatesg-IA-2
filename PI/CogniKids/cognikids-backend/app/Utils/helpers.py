"""
Funções utilitárias para o sistema CogniKids
"""

from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import jsonify
import functools

def validate_object_id(id_string):
    """
    Valida se uma string é um ObjectId válido do MongoDB
    
    Args:
        id_string (str): String a ser validada
        
    Returns:
        bool: True se válido, False caso contrário
    """
    try:
        ObjectId(id_string)
        return True
    except (InvalidId, TypeError):
        return False

def validate_required_fields(data, required_fields):
    """
    Valida se todos os campos obrigatórios estão presentes nos dados
    
    Args:
        data (dict): Dados a serem validados
        required_fields (list): Lista de campos obrigatórios
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not data:
        return False, "Dados não fornecidos"
    
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return False, f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
    
    return True, ""

def convert_objectid_to_string(data):
    """
    Converte ObjectIds para strings em um dicionário ou lista de dicionários
    
    Args:
        data: Dicionário ou lista de dicionários
        
    Returns:
        dict/list: Dados com ObjectIds convertidos para strings
    """
    if isinstance(data, list):
        return [convert_objectid_to_string(item) for item in data]
    
    if isinstance(data, dict):
        converted = {}
        for key, value in data.items():
            if isinstance(value, ObjectId):
                converted[key] = str(value)
            elif isinstance(value, dict):
                converted[key] = convert_objectid_to_string(value)
            elif isinstance(value, list):
                converted[key] = convert_objectid_to_string(value)
            else:
                converted[key] = value
        return converted
    
    return data

def handle_errors(f):
    """
    Decorator para tratamento consistente de erros
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                "status": "erro",
                "message": "Erro interno do servidor",
                "error": str(e)
            }), 500
    return decorated_function

def create_success_response(message="Operação realizada com sucesso", data=None):
    """
    Cria uma resposta padrão de sucesso
    """
    response = {
        "status": "sucesso",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response

def create_error_response(message="Erro na operação", status_code=400):
    """
    Cria uma resposta padrão de erro
    """
    return jsonify({
        "status": "erro",
        "message": message
    }), status_code