import logging
from conexao import DATABASE_NAME, COLLECTION_NAME

def run_aggregations(client):
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    logging.info("Executando agregações...")

    # ============================================================
    # 🔹 PIPELINE 1 — Top gêneros por quantidade de filmes
    # ============================================================

    pipeline_genres = [
        {
            "$project": {
                "Genre": {
                    "$split": ["$Genre", ", "]  # separa múltiplos gêneros
                },
                "IMDB_Rating": 1
            }
        },
        { "$unwind": "$Genre" },
        {
            "$group": {
                "_id": "$Genre",
                "media_rating": { "$avg": "$IMDB_Rating" },
                "quantidade": { "$sum": 1 }
            }
        },
        { "$sort": { "quantidade": -1 } }
    ]

    logging.info("📌 Top gêneros por quantidade:")
    for doc in collection.aggregate(pipeline_genres):
        logging.info(doc)

    # ============================================================
    # 🔹 PIPELINE 2 — Média IMDB por categoria de duração
    # curto (<= 90), médio (91-120), longo (> 120)
    # ============================================================

    pipeline_runtime = [
        {
            "$addFields": {
                "DurationInt": {
                    "$toInt": {
                        "$replaceAll": {
                            "input": "$Duration",
                            "find": " min",
                            "replacement": ""
                        }
                    }
                }
            }
        },
        {
            "$addFields": {
                "categoria_runtime": {
                    "$switch": {
                        "branches": [
                            {
                                "case": { "$lte": ["$DurationInt", 90] },
                                "then": "curto"
                            },
                            {
                                "case": { 
                                    "$and": [
                                        { "$gt": ["$DurationInt", 90] },
                                        { "$lte": ["$DurationInt", 120] }
                                    ]
                                },
                                "then": "medio"
                            }
                        ],
                        "default": "longo"
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$categoria_runtime",
                "media_rating": { "$avg": "$IMDB_Rating" },
                "quantidade": { "$sum": 1 }
            }
        },
        { "$sort": { "quantidade": -1 } }
    ]

    logging.info("📌 Média IMDB por categoria de duração:")
    for doc in collection.aggregate(pipeline_runtime):
        logging.info(doc)
