# IMDB Top 1000 — Pipeline Analítico com MongoDB Atlas e Python
## Arquitetura do Projeto
### MongoDB-IMDB-Project
│
├── **.env**
├── **README.md**
├── **requirements.txt**
│
├── **main.py** >> Controla a ordem de execução
├── **conexao.py** >> Monta a connection string MongoDB, carregar usuário, senha e host do .env, realizar o comando ping para validar a conexão e retornar o client já conectado
│
├── **data/**
│   └── **IMDB top 1000.csv**
│
├── **services/**
│   ├── **import_data.py** >> carrega o CSV, usa Pandas para estruturar a tabela, converte para JSON e insere no MongoDB via insert_many
│   ├── **queries.py** >> Consultas como contagem de filmes com nota > 9, filtros simples e pesquisas específicas
│   ├── **aggregations.py** >> Inclui pipelines relevantes para IA e ciência de dados
│   ├── **indexes.py** >> Cria índices para otimizar consultas
│   └── **clean_dataframe.py** >> Funções para normalizar nomes das colunas, converter tipos numéricos, além de padronizar formato dos dados
│
└── **utils/**
    └── **logging_config.py** >> Define o formato padrão dos logs do projeto: horário, tipo do log e mensagem
|
└──**prints/**
    

