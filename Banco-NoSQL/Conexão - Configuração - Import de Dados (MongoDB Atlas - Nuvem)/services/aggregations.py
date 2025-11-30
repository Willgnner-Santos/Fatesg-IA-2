import logging
from conexao import DATABASE_NAME, COLLECTION_NAME

def run_aggregations(client):
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    logging.info("Executando agregações...")


    pipeline_genres = [
        {"$group": {"_id": "$genre", "media_rate": {"$avg": "$rate"}, "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}
    ]

    logging.info("Top gêneros:")
    for doc in collection.aggregate(pipeline_genres):
        logging.info(doc)

    pipeline_runtime = [
        {"$addFields": {
            "categoria_runtime": {
                "$switch": {
                    "branches": [
                        {"case": {"$lt": ["$runtime", 90]}, "then": "curto"},
                        {"case": {"$and": [{"$gte": ["$runtime", 90]}, {"$lte": ["$runtime", 120]}]}, "then": "medio"},
                        {"case": {"$gt": ["$runtime", 120]}, "then": "longo"}
                    ],
                    "default": "indefinido"
                }
            }
        }},
        {"$group": {
            "_id": "$categoria_runtime",
            "media_rate": {"$avg": "$rate"},
            "quantidade": {"$sum": 1}
        }},
        {"$sort": {"quantidade": -1}}
    ]

    logging.info("Categorias de duração:")
    for doc in collection.aggregate(pipeline_runtime):
        logging.info(doc)
