import pymongo
import pandas as pd
import numpy as np
import random

NOMES_BRASILEIROS = [
    "Ana Silva", "Bruno Santos", "Carla Oliveira", "Daniel Costa", "Eduarda Lima",
    "Felipe Rocha", "Gabriela Gomes", "Hugo Alves", "Isabela Pereira", "João Souza",
    "Laura Mendes", "Marcelo Nunes", "Natália Vieira", "Pedro Barbosa", "Rafaela Fernandes",
    "Thiago Dantas", "Vitória Castro", "Guilherme Freitas", "Juliana Ribeiro", "Lucas Pires",
    "Mariana Dias", "Ricardo Azevedo", "Sofia Correa", "Vitor Vasconcelos", "Aline Melo",
    "Cássio Bernardes", "Duda Lemos", "Elias Ramos", "Fernanda Matos", "Gustavo Bezerra"
]

CARGOS_TI = [
    "Diretor TI",
    "Gerente Projetos",
    "Coordenador TI",
    "Analista Senior",
    "Analista Pleno",
    "Analista Junior",
    "Dev Front-End",
    "Dev Back-End",
    "Dev FullStack",
    "Dev Mobile",
    "Dev Python",
    "Dev Java",
    "Dev C#",
    "Dev PHP",
    "DBA",
    "Especialista Cloud",
    "Cybersecurity",
    "Estagiário TI",
]

N_PONTOS = 1000                         
BASE_SALARIAL_MIN = 25000.00                    
AUMENTO_POR_ANO = 1500.00                        
DESVIO_PADRAO = 18000.00                    

print("→ Gerando idades e salários...")

idades = np.random.randint(22, 66, N_PONTOS)
ruido = np.random.normal(0, DESVIO_PADRAO, N_PONTOS)
salarios_estimados = BASE_SALARIAL_MIN + (AUMENTO_POR_ANO * idades) + ruido
salarios = np.maximum(salarios_estimados, 18000)

print("→ Gerando nomes...")
nomes = [random.choice(NOMES_BRASILEIROS) for _ in range(N_PONTOS)]

print("→ Gerando cargos...")
cargos = [random.choice(CARGOS_TI) for _ in range(N_PONTOS)]

print("→ Criando DataFrame...")
df_salarios = pd.DataFrame({
    'nome': nomes,
    'idade': idades,
    'salario': np.round(salarios, 2),
    'cargo': cargos
})

print("\n--- Amostra dos Dados Gerados ---")
print(df_salarios.head(10))

dados_para_mongo = df_salarios.to_dict(orient="records")

print("\n→ Conectando ao MongoDB...")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["startup"]
collection = db["funcionarios"]

print("→ Limpando coleção antiga...")
collection.delete_many({})

print("→ Inserindo dados no MongoDB...")

for index, doc in enumerate(dados_para_mongo, start=1):
    collection.insert_one(doc)

    if index % 100 == 0:
        print(f"   {index} documentos inseridos...")

print("\n✔ Todos os dados foram inseridos com sucesso!")
print(f"Total de registros: {collection.count_documents({})}")

client.close()
print("✔ Conexão fechada.")
