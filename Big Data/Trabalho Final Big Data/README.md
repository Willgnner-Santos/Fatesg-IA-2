# Pipeline de Dados End-to-End para Análise de E-commerce

## 1. Objetivo do Projeto

Este projeto demonstra a construção de uma pipeline de dados completa e escalável, desde a ingestão de dados brutos até a criação de um dashboard interativo. O objetivo foi aplicar técnicas modernas de engenharia de dados para analisar um grande volume de informações de e-commerce, superando os desafios impostos pela escala dos dados.

O principal desafio foi lidar com um dataset de aproximadamente **40 milhões de linhas** na tabela principal, distribuído em cinco tabelas relacionais. Este volume inviabiliza o uso de ferramentas tradicionais e exige uma arquitetura baseada em nuvem para processamento e análise eficientes.

## 2. Arquitetura da Pipeline

A solução foi desenvolvida utilizando um ecossistema de ferramentas do Google Cloud, garantindo performance, escalabilidade e baixo custo.

* **Origem e Armazenamento Inicial:** Os 5 arquivos CSV com os dados brutos foram hospedados no **Google Drive**, servindo como um repositório central acessível pela nuvem.

* **Processamento e Limpeza (ETL):** O **Google Colab** foi utilizado como ambiente de desenvolvimento interativo. O framework **Pandas** foi o principal responsável pela limpeza e transformação dos dados, incluindo a correção de tipos, tratamento de valores nulos e remoção de duplicados.

* **Armazenamento (Data Warehouse):** Após o tratamento, os dados limpos foram carregados no **Google BigQuery**, um Data Warehouse serverless. Para otimizar a performance e simplificar a camada de análise, uma **VIEW** foi criada utilizando **SQL** para unir as cinco tabelas em um único modelo denormalizado.

* **Visualização e Análise (BI):** O **Looker Studio** foi conectado diretamente à VIEW no BigQuery para a criação de um dashboard dinâmico, permitindo a exploração dos KPIs e insights do negócio.

## 3. Frameworks e Ferramentas Utilizadas

* **Linguagens:** Python, SQL
* **Frameworks e Bibliotecas:** Pandas
* **Plataforma de Nuvem:** Google Cloud Platform (GCP)
* **Ferramentas Principais:**
    * **Google Colab:** Ambiente de processamento e execução do notebook.
    * **Google Drive:** Armazenamento dos dados brutos.
    * **Google BigQuery:** Data Warehouse para os dados tratados.
    * **Looker Studio:** Ferramenta de Business Intelligence para visualização.

## 4. Como Executar o Projeto

1.  **Pré-requisitos:** É necessário ter uma conta Google com acesso ao Drive, Colab e um projeto no Google Cloud com a API do BigQuery ativada.
2.  **Upload:** Carregar os arquivos CSV originais para uma pasta no Google Drive.
3.  **Processamento:** Executar o notebook Jupyter (`.ipynb`) no Google Colab. O notebook irá guiar pela limpeza dos dados e carregamento dos mesmos no BigQuery.
4.  **Modelagem:** Executar o script SQL (`.sql`) no BigQuery para criar a `VIEW` que une as tabelas.
5.  **Visualização:** Conectar o Looker Studio como uma nova fonte de dados à `VIEW` criada no BigQuery para desenvolver os relatórios.

## 5. Fonte dos Dados

O dataset original está publicamente disponível na plataforma Kaggle e pode ser acedido através do seguinte link:

* **Fonte:** [Synthetic E-commerce Relational Dataset - Kaggle](https://www.kaggle.com/datasets/naelaqel/synthetic-e-commerce-relational-dataset?resource=download)

## 6. Resultados e Dashboard

O resultado final é um dashboard interativo no Looker Studio que apresenta os principais KPIs de negócio, como Receita Total, Ticket Médio, Taxa de Conversão, Vendas por Categoria e Análise de Clientes. A arquitetura implementada permite que o dashboard realize consultas em tempo real sobre milhões de linhas de forma eficiente.

<img width="1197" height="899" alt="image" src="https://github.com/user-attachments/assets/9a25d4f1-4334-4226-a96d-cd77f8f17782" />
