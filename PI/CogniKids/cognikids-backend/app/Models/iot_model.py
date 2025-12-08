# app/models/iot_model.py
from bson.objectid import ObjectId
import datetime

class DispositivoIoTModel:
    """
    Representa um dispositivo IoT no sistema.
    """
    @staticmethod
    def get_schema():
        return {
            "aluno_id": ObjectId(), # ID do aluno ao qual o dispositivo está vinculado
            "ultima_conexao": datetime.datetime.utcnow(),
            "status": "ativo" # Ex: ativo, inativo, bateria_baixa
        }

class RegistroIoTModel:
    """
    Representa um único registro de dados biométricos enviado por um dispositivo.
    """
    @staticmethod
    def get_schema(dispositivo_id, aluno_id, dados_biometricos):
        return {
            "dispositivo_id": ObjectId(dispositivo_id),
            "aluno_id": ObjectId(aluno_id),
            "data_hora": datetime.datetime.utcnow(),
            "dados_biometricos": dados_biometricos # Objeto com os dados (ex: batimento, temp)
        }