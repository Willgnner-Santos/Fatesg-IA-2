import pandas as pd
import json
import logging

from services.clean_dataframe import clean_dataframe
from conexao import DATABASE_NAME, COLLECTION_NAME

# CAMINHO DO CSV
csv_path = r"C:\Users\Luca\Documents\Fatesg-IA-2\Banco-NoSQL\Conexão - Configuração - Import de Dados (MongoDB Atlas - Nuvem)\data\IMDBtop1000.csv"

def import_csv_to_mongodb(client):
    try:
        logging.info(f"Lendo arquivo CSV: {csv_path}")
        df = pd.read_csv(csv_path)

        df = clean_dataframe(df)
        data_json = json.loads(df.to_json(orient="records"))

        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        if "poster_link" in df.columns:
            logging.info("Criando índice único...")
            collection.create_index([("poster_link", 1)], unique=True)

        logging.info("Inserindo documentos...")
        collection.insert_many(data_json, ordered=False)

        logging.info("Importação concluída com sucesso!")

    except Exception as e:
        logging.error(f"Erro na importação: {e}")
