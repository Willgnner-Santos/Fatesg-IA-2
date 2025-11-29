# Primeira parte
import pandas as pd
import pymongo
import urllib.parse

# Definir o caminho do arquivo CSV
csv_path = r"C:\Users\Davi\Downloads\IMDB top 1000.csv"

# Ler o CSV usando Pandas
df = pd.read_csv(csv_path)

# Segunda parte
import pymongo
import urllib.parse

# Definir usuário e senha
username = "davi"
password = "337766@Go"

# Codificar a senha (caso tenha caracteres especiais)
password_encoded = urllib.parse.quote_plus(password)

# Criar a URI corretamente formatada
MONGO_URI = f"mongodb+srv://{username}:{password_encoded}@atividade.xxlmfo1.mongodb.net/?appName=atividade"

# Conectar ao MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)

# Acessar o banco e a coleção
db = client["conexao"]
collection = db["dados"]

print("Conexão com MongoDB Atlas estabelecida!")

# Terceira parte

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

# No caso funciona rodando no próprio Banco na Nuvem

# Mostra todos os documentos onde o campo Genre é exatamente "Drama".
{ "Genre": "Drama" }

# Filmes com nota (Rate) maior que 9
{ "Rate": { "$gt": 9 } }

# Você também pode combinar com expressões regulares para buscas por texto:
{ "Description": { "$regex": "prison", "$options": "i" } }