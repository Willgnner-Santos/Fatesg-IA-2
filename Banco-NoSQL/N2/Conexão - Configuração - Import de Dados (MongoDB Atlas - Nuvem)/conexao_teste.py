import pandas as pd
import pymongo
import urllib.parse

# Definir o caminho do arquivo CSV
csv_path = 'IMDB top 1000.csv'

# Ler o CSV usando Pandas
df = pd.read_csv(csv_path)

print(df.head(6))

import pymongo
import certifi

MONGO_URI = "mongodb+srv://felipefatesg_db_user:1234@chatbot.mrcuhu0.mongodb.net/?appName=Chatbot"

client = pymongo.MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

client.admin.command('ping')

db = client["filmes"]
collection = db["filmes-series"]

print("✅ Conexão estabelecida!")

# Converte o DataFrame (df) em uma lista de dicionários, onde cada linha vira um "registro" (record) separado.
# df.to_dict() → transforma o DataFrame em um dicionário.
# orient="records" → define o formato da conversão: cada linha = 1 dicionário (ideal para inserir no MongoDB).
dados_json = df.to_dict(orient="records")

# Ou seja: orient="records" instrui o pandas a gerar uma lista de documentos JSON,
# cada um representando uma linha da tabela, que o MongoDB entende perfeitamente.

# Insere todos os documentos (dicionários) da lista 'dados_json' dentro da coleção MongoDB de uma só vez.
# 'collection' → é o objeto que representa a coleção (tabela) no banco MongoDB.
# 'insert_many()' → comando do PyMongo que insere múltiplos documentos de uma vez (em lote).
# 'dados_json' → é a lista de dicionários criada antes (cada item = um documento/linha).
collection.insert_many(dados_json)

print(" Dados enviados para o MongoDB Atlas com sucesso!")

"""Consultas no Banco"""

for doc in collection.find({"Genre": "Drama"}):
    print(doc["Title"], "-", doc["Rate"])

# Retorna todos os filmes onde o campo "Genre" é "Drama".
# Você pode alterar para "Action", "Comedy", etc.

for doc in collection.find({"Rate": {"$gt": 8.5}}):
    print(doc["Title"], "-", doc["Rate"])

# O operador $gt significa greater than (maior que).
# Mostra filmes com nota superior a 8.5 no IMDB.

top5 = collection.find().sort("Rate", -1).limit(5)
for doc in top5:
    print(doc["Title"], "-", doc["Rate"])

# Ordena do maior para o menor (-1) e mostra apenas 5 resultados.

query = {"Genre": "Drama", "Metascore": {"$gt": 90}}
for doc in collection.find(query, {"Title": 1, "Metascore": 1, "_id": 0}):
    print(doc)

# Filtra por dois critérios: gênero e metascore alto.
# O segundo parâmetro {} define quais campos mostrar (1 = incluir, 0 = excluir).

count = collection.count_documents({"Certificate": "R"})
print("Total de filmes com classificação R:", count)

## Conta quantos documentos possuem o valor "R" no campo "Certificate".

from datetime import datetime

print("\n" + "="*60)
print("CONSULTAS SIMPLES (RESUMIDAS)")
print("="*60)

# Consulta 1: Filmes de um gênero específico
print("\n1️⃣ Filmes do gênero Drama (primeiros 5):")
drama_count = 0
for doc in collection.find({"Genre": "Drama"}).limit(5):
    print(f"  • {doc.get('Title', 'N/A')} - {doc.get('Rate', 'N/A')} ⭐")
    drama_count += 1
if drama_count == 0:
    print("  Nenhum filme encontrado.")

# Consulta 2: Filmes com nota superior a 8.5
print("\n2️⃣ Filmes com nota IMDB maior que 8.5 (primeiros 5):")
for doc in collection.find({"Rate": {"$gt": 8.5}}).limit(5):
    print(f"  • {doc.get('Title', 'N/A')} - {doc.get('Rate', 'N/A')} ⭐")

# Consulta 3: Top 5 filmes por nota
print("\n3️⃣ Top 5 filmes com maior nota:")
top5 = collection.find().sort("Rate", -1).limit(5)
for i, doc in enumerate(top5, 1):
    print(f"  {i}. {doc.get('Title', 'N/A')} - {doc.get('Rate', 'N/A')} ⭐")

# Consulta 4: Filmes com múltiplos critérios
print("\n4️⃣ Filmes de Drama com Metascore maior que 75 (primeiros 5):")
query = {"Genre": "Drama", "Metascore": {"$gt": 75}}
results = collection.find(query, {"Title": 1, "Metascore": 1, "Rate": 1, "_id": 0}).limit(5)
for doc in results:
    print(f"  • {doc}")

# Consulta 5: Contagem de documentos por certificado
print("\n5️⃣ Total de filmes por certificado:")
certs = collection.distinct("Certificate")
for cert in certs[:5]:
    count = collection.count_documents({"Certificate": cert})
    print(f"  • {cert}: {count} filmes")

# Consulta 6: Busca por texto (regex)
print("\n6️⃣ Filmes com 'prison' na descrição:")
prison_movies = collection.find(
    {"Description": {"$regex": "prison", "$options": "i"}}
).limit(3)
count_prison = 0
for doc in prison_movies:
    print(f"  • {doc.get('Title', 'N/A')}")
    count_prison += 1
if count_prison == 0:
    print("  Nenhum filme encontrado com 'prison' na descrição.")

print("\n" + "="*60)
print("OPERAÇÕES DE AGREGAÇÃO")
print("="*60)

# Agregação 1: Média de notas por gênero
print("\n1️⃣ Média de notas IMDB por gênero (top 5):")
pipeline1 = [
    {"$group": {"_id": "$Genre", "media_rate": {"$avg": "$Rate"}}},
    {"$sort": {"media_rate": -1}},
    {"$limit": 5}
]
for doc in collection.aggregate(pipeline1):
    print(f"  • {doc['_id']}: {doc['media_rate']:.2f} ⭐")

# Agregação 2: Quantidade de filmes por certificado
print("\n2️⃣ Quantidade de filmes por certificado:")
pipeline2 = [
    {"$group": {"_id": "$Certificate", "quantidade": {"$sum": 1}}},
    {"$sort": {"quantidade": -1}}
]
for doc in collection.aggregate(pipeline2):
    print(f"  • {doc['_id']}: {doc['quantidade']} filmes")

# Agregação 3: Filmes com maior Metascore por gênero
print("\n3️⃣ Filme com maior Metascore por gênero (top 3):")
pipeline3 = [
    {"$match": {"Metascore": {"$ne": None, "$gt": 0}}},
    {"$sort": {"Metascore": -1}},
    {"$group": {
        "_id": "$Genre",
        "title": {"$first": "$Title"},
        "metascore": {"$first": "$Metascore"}
    }},
    {"$limit": 3}
]
for doc in collection.aggregate(pipeline3):
    metascore = doc.get('metascore')
    if metascore is not None:
        print(f"  • {doc['_id']}: {doc['title']} (Metascore: {int(metascore)})")
    else:
        print(f"  • {doc['_id']}: {doc['title']} (Metascore não disponível)")

# Agregação 4: Distribuição de faixas de notas
print("\n4️⃣ Distribuição de faixas de notas IMDB:")
pipeline4 = [
    {"$bucket": {
        "groupBy": "$Rate",
        "boundaries": [6, 7, 8, 8.5, 9, 10],
        "default": "Não classificado",
        "output": {"quantidade": {"$sum": 1}}
    }},
    {"$sort": {"_id": 1}}
]
for doc in collection.aggregate(pipeline4):
    if isinstance(doc['_id'], (int, float)):
        faixa = f"{doc['_id']}-{doc['_id']+1}"
    else:
        faixa = doc['_id']
    print(f"  • Notas {faixa}: {doc['quantidade']} filmes")

print("\n" + "="*60)
print("CRIAÇÃO E ANÁLISE DE ÍNDICES")
print("="*60)

# Criar índices para melhorar performance
print("\n📑 Criando índices...")

# Índice 1: Campo Rate (notas)
collection.create_index("Rate")
print(f"  ✓ Índice criado em 'Rate'")

# Índice 2: Campo Genre
collection.create_index("Genre")
print(f"  ✓ Índice criado em 'Genre'")

# Índice 3: Campo Certificate
collection.create_index("Certificate")
print(f"  ✓ Índice criado em 'Certificate'")

# Índice 4: Índice composto (Genre + Rate)
collection.create_index([("Genre", 1), ("Rate", -1)])
print(f"  ✓ Índice composto criado em 'Genre' + 'Rate'")

# Índice 5: Índice de texto para busca por descrição
collection.create_index([("Description", "text")])
print(f"  ✓ Índice de texto criado em 'Description'")

# Listar todos os índices
print("\n📊 Índices existentes na coleção:")
indexes = collection.list_indexes()
for idx in indexes:
    print(f"  • {idx['name']}: {idx['key']}")

print("\n" + "="*60)
print("ANÁLISE DE PERFORMANCE DE QUERIES")
print("="*60)

# Query com índice (rápida)
print("\n🚀 Query com índice (Rate > 8.5):")
query_result = collection.find({"Rate": {"$gt": 8.5}}).explain()
print(f"  Documentos examinados: {query_result['executionStats']['totalDocsExamined']}")
print(f"  Documentos retornados: {query_result['executionStats']['nReturned']}")

# Query com múltiplos critérios usando índice composto
print("\n🚀 Query com índice composto (Genre + Rate):")
query_result2 = collection.find({"Genre": "Drama", "Rate": {"$gt": 8}}).explain()
print(f"  Documentos examinados: {query_result2['executionStats']['totalDocsExamined']}")
print(f"  Documentos retornados: {query_result2['executionStats']['nReturned']}")

print("\n" + "="*60)
print("📈 RESUMO DA ANÁLISE")
print("="*60)

total_docs = collection.count_documents({})
print(f"Total de documentos: {total_docs}")

avg_rate = collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$Rate"}}}])
avg_value = list(avg_rate)[0]['avg']
print(f"Nota média IMDB: {avg_value:.2f} ⭐")

max_rate = collection.find_one(sort=[("Rate", -1)])
print(f"Filme com maior nota: {max_rate['Title']} ({max_rate['Rate']} ⭐)")

max_metascore = collection.find_one({"Metascore": {"$ne": None}}, sort=[("Metascore", -1)])
if max_metascore:
    print(f"Filme com maior Metascore: {max_metascore['Title']} ({int(max_metascore['Metascore'])})")

print("\n✅ Análise completa finalizada!")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")