# Projeto ETL com Python e MongoDB Atlas - IMDB Top 1000

Este projeto demonstra um processo completo de **ETL (Extract, Transform, Load)** utilizando Python. O script lê um dataset de filmes (CSV), processa os dados e carrega-os para um cluster na nuvem (MongoDB Atlas). Além da carga de dados, o projeto inclui exemplos práticos de como realizar consultas complexas numa base de dados NoSQL.

## 📋 Funcionalidades

O script `conexao-teste.ipynb` realiza as seguintes operações:

1.  **Extração**: Leitura de dados do ficheiro `IMDB top 1000.csv` utilizando a biblioteca Pandas.
2.  **Transformação**: Conversão do DataFrame para um formato de lista de dicionários (JSON), compatível com o MongoDB.
3.  **Carregamento**: Inserção em lote (`insert_many`) de todos os registos na coleção `filmes-series` na nuvem.
4.  **Consultas**: Execução de diversas queries para análise de dados.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pandas**: Manipulação e análise de dados.
* **PyMongo**: Driver oficial do MongoDB para Python.
* **MongoDB Atlas**: Serviço de base de dados como serviço (DBaaS).
* **Certifi**: Fornece certificados de raiz da Mozilla para validação SSL (essencial para evitar erros de conexão).
* **Dnspython**: Toolkit DNS para python.

## 🚀 Configuração e Instalação

### 1. Instalar Dependências
Execute o seguinte comando no seu terminal ou numa célula do notebook para instalar as bibliotecas necessárias:

```bash
pip install pandas pymongo certifi dnspython