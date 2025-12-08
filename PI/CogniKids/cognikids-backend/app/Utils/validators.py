"""
Validadores comuns para o sistema CogniKids
"""

from bson.objectid import ObjectId
from bson.errors import InvalidId

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

def validate_user_type(user_type, allowed_types):
    """
    Valida se o tipo de usuário está entre os permitidos
    
    Args:
        user_type (str): Tipo do usuário
        allowed_types (list): Lista de tipos permitidos
        
    Returns:
        bool: True se válido, False caso contrário
    """
    return user_type in allowed_types

def validate_email(email):
    """
    Validação básica de email
    
    Args:
        email (str): Email a ser validado
        
    Returns:
        bool: True se válido, False caso contrário
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_required_fields(data, required_fields):
    """
    Valida se todos os campos obrigatórios estão presentes
    
    Args:
        data (dict): Dados a serem validados
        required_fields (list): Lista de campos obrigatórios
        
    Returns:
        tuple: (bool, list) - (is_valid, missing_fields)
    """
    if not data:
        return False, required_fields
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    
    return len(missing_fields) == 0, missing_fields