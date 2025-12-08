# app/models/support_kit_model.py
from bson.objectid import ObjectId
import datetime

class SupportKitModel:
    """
    Define a estrutura para o Kit de Apoio de um aluno.
    """
    @staticmethod
    def get_schema(aluno_id, updated_by_id):
        return {
            "aluno_id": ObjectId(aluno_id),
            "neurodivergencia": "",
            "interesses": [], # Lista de strings, ex: ["Desenho", "Dinossauros"]
            "sensibilidades": [], # Lista de strings, ex: ["Ruídos altos", "Luzes fortes"]
            "estrategias_calmantes": "", # Campo de texto livre
            "contatos_emergencia": [
                # { "nome": "...", "relacao": "...", "telefone": "..." }
            ],
            "last_updated": datetime.datetime.utcnow(),
            "updated_by": ObjectId(updated_by_id) # ID do pai/responsável
        }