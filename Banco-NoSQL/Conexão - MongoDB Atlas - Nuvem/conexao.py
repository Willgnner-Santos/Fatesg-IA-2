import pymongo
import urllib.parse
import os
import logging

from dotenv import load_dotenv
load_dotenv()


username = os.getenv("MONGO_USER", "Aluno_Luca")
password = os.getenv("MONGO_PASS", "cod@96")
CLUSTER_URI_PART = os.getenv("CLUSTER_URI", "cluster0.6b5gbtc.mongodb.net/?appName=Cluster0")

DATABASE_NAME = "IMDB_Analytics_Willgner"
COLLECTION_NAME = "Top_1000_Movies"

def connect_to_mongodb():
    try:
        logging.info("Conectando ao MongoDB Atlas...")

        password_encoded = urllib.parse.quote_plus(password)
        MONGO_URI = f"mongodb+srv://{username}:{password_encoded}@{CLUSTER_URI_PART}"

        client = pymongo.MongoClient(MONGO_URI)
        client.admin.command("ping")

        logging.info("Conexão realizada com sucesso!")

        return client

    except Exception as e:
        logging.error(f"Erro crítico de conexão: {e}")
        return None

