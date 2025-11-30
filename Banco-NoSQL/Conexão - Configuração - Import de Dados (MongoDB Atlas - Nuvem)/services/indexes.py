import logging
from conexao import DATABASE_NAME, COLLECTION_NAME

def create_indexes(client):
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    logging.info("Criando índices...")

    collection.create_index([("genre", 1)])
    collection.create_index([("rate", -1)])
    collection.create_index([("runtime", 1)])

    logging.info("Índices criados com sucesso!")
