import logging
from utils.logging_config import setup_logging
from conexao import connect_to_mongodb
from services.import_data import import_csv_to_mongodb
from services.queries import run_basic_queries
from services.aggregations import run_aggregations
from services.indexes import create_indexes

setup_logging()

client = connect_to_mongodb()

if client:
    # Se ainda não importou CSV:
    # import_csv_to_mongodb(client)

    run_basic_queries(client)
    run_aggregations(client)
    create_indexes(client)
    import_csv_to_mongodb(client)


    client.close()
    logging.info("Fim da execução.")
