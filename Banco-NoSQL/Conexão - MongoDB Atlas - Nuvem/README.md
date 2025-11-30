# Pipeline Analítico NoSQL com MongoDB Atlas — IMDB Top 1000

Este projeto foi desenvolvido para a disciplina de **Banco de Dados Não-Relacional**, com o objetivo de construir um pipeline completo de análise usando:

- **MongoDB Atlas (nuvem)**
- **PyMongo**
- **Pandas**
- **Python 3**

O dataset utilizado foi o **IMDB Top 1000**, contendo informações de filmes como título, gênero, ano, duração, nota IMDB, Metascore e descrição.  
O projeto realiza **importação de dados, consultas, agregações e criação de índices**, documentando todo o processo com evidências.

---

## Arquitetura do Projeto

MongoDB-IMDB-Project
│
├── .env                       # Variáveis sensíveis 
├── README.md                  # Documentação completa do projeto
├── requirements.txt           # Dependências do Python
│
├── main.py                    # Controla a ordem de execução do pipeline
├── conexao.py                 # Gera a connection string, carrega variáveis e retorna o client conectado
│
├── data/
│   └── IMDB top 1000.csv      # Dataset original usado no projeto
│
├── services/
│   ├── import_data.py         # Lê CSV, converte com pandas e envia ao MongoDB via insert_many
│   ├── queries.py             # Consultas simples e intermediárias
│   ├── aggregations.py        # Pipelines analíticas do MongoDB (Aggregation Framework)
│   └── indexes.py             # Criação de índices para otimização
│
├── utils/
│   └── logging_config.py      # Configuração dos logs
│
└── entregas_em_png/
    ├── Dados_do_csv_inseridos_no_Cluster.png
    ├── indexes_1.png
    ├── indexes_2.png
    ├── main.py_rodando.png
    └── Uso_das_pipelines.png

---

# Como Executar o Projeto

## Clone o repositório
```bash
git 
cd 
```

## 2️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

## 3️⃣ Configure o arquivo `.env`
Crie o arquivo na raiz do projeto:

```
MONGO_USER=Aluno_Luca
MONGO_PASS=sua_senha_aqui
CLUSTER_URI=cluster0.6b5gbtc.mongodb.net/?appName=Cluster0
```

⚠️ Atenção: **nunca suba o .env para o GitHub**.

## 4️⃣ Execute o pipeline completo
```bash
python main.py
```

Esse script executa:

- Conexão com o Atlas  
- Importação do CSV  
- Consultas  
- Agregações  
- Criação de índices  
- Geração de logs  

---

# 📸 Evidências da Execução

As evidências solicitadas pelo professor estão disponíveis na pasta `/prints`.

Elas incluem:

- Conexão no MongoDB Atlas  
- Documentos inseridos na coleção  
- Índices criados  
- Execução do main.py  
- Agregações funcionando  
- Prints do Compass (opcional)  

---

# 🔍 Consultas Realizadas (Queries)

### ✔ 1. Contar filmes com IMDB_Rating maior que 9
```python
collection.count_documents({"IMDB_Rating": {"$gt": 9}})
```

### ✔ 2. Filmes lançados antes de 1980
```python
{"Released_Year": {"$lt": 1980}}
```

### ✔ 3. Filmes do gênero “Action”
```python
{"Genre": {"$regex": "Action"}}
```

### ✔ 4. Filmes com mais de 500.000 votos
```python
{"No_of_Votes": {"$gt": 500000}}
```

---

# 📊 Pipelines de Agregação (Aggregation Framework)

## 🔹 1. Média de Metascore por Categoria de Duração  
Categorias:  
- **curto** → ≤ 90 min  
- **médio** → 91 a 120 min  
- **longo** → > 120 min  

```json
[
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
      "durationCategory": {
        "$switch": {
          "branches": [
            { "case": { "$lte": ["$DurationInt", 90] }, "then": "curto" },
            { "case": { "$and": [ { "$gt": ["$DurationInt", 90] }, { "$lte": ["$DurationInt", 120] } ] }, "then": "médio" }
          ],
          "default": "longo"
        }
      }
    }
  },
  {
    "$group": {
      "_id": "$durationCategory",
      "avgMetascore": { "$avg": "$Meta_score" },
      "countMovies": { "$sum": 1 }
    }
  },
  { "$sort": { "_id": 1 } }
]
```

---

## 🔹 2. Top Gêneros por Quantidade de Filmes

```json
[
  {
    "$project": {
      "Genre": { "$split": ["$Genre", ", "] },
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
```

---

# ⚡ Índices Criados

Para otimizar consultas e melhorar a performance, os seguintes índices foram criados:

### ✔ Índice em `Genre`
```python
collection.create_index([("Genre", 1)])
```

### ✔ Índice em `IMDB_Rating`
```python
collection.create_index([("IMDB_Rating", -1)])
```

### ✔ Índice em `Duration`
```python
collection.create_index([("Duration", 1)])
```

Esses índices reduzem o custo de operações de busca e ordenação.  
A evidência visual está disponível em:

```
prints/indexes_1.png
prints/indexes_2.png
```

---

# 📂 Logs

Todos os logs gerados pelo pipeline estão na pasta:

```
/logs/execution.log
```

Eles incluem:

- Tentativas de conexão  
- Sucesso/falha em operações  
- Queries executadas  
- Agregações  
- Índices criados  

---

# 👨‍💻 Autor

**Luca Atanazio Evangelista**  
Estudante de Inteligência Artificial — FATESG

# 👨‍🏫 Professor  
**Willgner**

---

# ✔ Conclusão

Este projeto demonstra a construção de um pipeline completo de análise NoSQL utilizando MongoDB Atlas e Python, com:

- Importação de dados
- Conversão Document-Oriented
- Consultas
- Agregações
- Índices
- Documentação e evidências

Está pronto para avaliação acadêmica e para ser usado como portfólio profissional.

```


