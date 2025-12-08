import csv
import os
from pymongo import MongoClient

# Conecta ao banco
client = MongoClient("mongodb://localhost:27017/cognikidsDB")
db = client.get_default_database()

collections_to_export = ['users', 'turmas', 'dispositivos', 'alerts']

print("Iniciando exportacao para diagnostico...")

for col_name in collections_to_export:
    data = list(db[col_name].find())
    
    if not data:
        print(f"AVISO: A colecao '{col_name}' esta vazia!")
        continue
        
    # Pega todos os campos possíveis (keys)
    keys = set()
    for doc in data:
        keys.update(doc.keys())
    keys = list(keys)
    
    filename = f"dump_{col_name}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for doc in data:
            writer.writerow(doc)
            
    print(f"OK: {col_name}: Exportado para {filename} ({len(data)} registros)")

print("\nExportacao concluida! Envie os arquivos 'dump_*.csv' para analise.")