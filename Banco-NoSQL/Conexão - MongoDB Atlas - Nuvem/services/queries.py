import logging
from conexao import DATABASE_NAME, COLLECTION_NAME

def run_basic_queries(client):
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    logging.info("Executando consultas básicas...")

    count_high_rate = collection.count_documents({"rate": {"$gt": 9.0}})
    logging.info(f"Filmes com nota > 9.0: {count_high_rate}")
