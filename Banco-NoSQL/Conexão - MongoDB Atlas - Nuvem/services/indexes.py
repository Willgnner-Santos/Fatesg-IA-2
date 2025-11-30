import logging
from conexao import DATABASE_NAME, COLLECTION_NAME

def create_indexes(client):
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    logging.info("Criando índices...")

    # Índice real — campo do dataset: "Genre"
    idx_genre = collection.create_index([("Genre", 1)])
    logging.info(f"Índice criado em Genre: {idx_genre}")

    # Índice real — campo do dataset: "IMDB_Rating"
    idx_rating = collection.create_index([("IMDB_Rating", -1)])
    logging.info(f"Índice criado em IMDB_Rating: {idx_rating}")

    # Índice real — converter Duration (ex: "142 min") para buscas
    idx_duration = collection.create_index([("Duration", 1)])
    logging.info(f"Índice criado em Duration: {idx_duration}")

    logging.info("Índices criados com sucesso!")
