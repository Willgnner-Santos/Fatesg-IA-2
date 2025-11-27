# Projeto de Chatbot e Geração de Perguntas com IA e MongoDB

Este projeto explora a integração entre **Python**, **MongoDB** e modelos de **Inteligência Artificial (LLMs)** da Hugging Face. O objetivo é criar pipelines de geração de texto que interagem com um banco de dados NoSQL para armazenar perguntas, respostas e insights analíticos simulados para um cenário de Recursos Humanos (RH).

O projeto é dividido em duas etapas: uma interação básica de perguntas e respostas e uma etapa avançada de engenharia de prompt para gerar perguntas analíticas estruturadas.

## 🚀 Funcionalidades

### Etapa 1: Chatbot Básico (`ChatcomMongoDB.py`)
* **Conexão com Banco de Dados:** Estabelece conexão com o MongoDB local.
* **Geração de Texto:** Utiliza o modelo `facebook/opt-1.3b` para responder a perguntas simples (ex: "O que é MongoDB?").
* **Armazenamento:** Salva a pergunta e a resposta gerada na coleção `conversas`.

### Etapa 2: Gerador de Perguntas Analíticas de RH (`ChatcomMongoDBpt2.py`)
* **Modelo Otimizado:** Utiliza a versão `facebook/opt-iml-1.3b` (Instruction Meta-Learning), mais adequada para seguir instruções.
* **Engenharia de Prompt:** Utiliza a técnica de *few-shot prompting* (dando exemplos) para guiar a IA a gerar uma lista de 15 perguntas analíticas focadas em dados de funcionários, salários e departamentos.
* **Refinamento de Parâmetros:** Ajuste de `temperature` (0.3) para respostas mais focadas e `repetition_penalty` para evitar loops.
* **Limpeza de Dados:** Script inclui lógica para formatar a saída e garantir que apenas a lista desejada seja processada.
* **Armazenamento Estruturado:** Salva o prompt original e a lista de perguntas geradas na coleção `perguntas_analiticas`.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **MongoDB** (Banco de dados NoSQL)
* **PyMongo** (Driver de conexão)
* **Hugging Face Transformers** (Biblioteca para uso dos modelos de IA)
* **PyTorch** (Backend para processamento dos modelos)

## 📋 Pré-requisitos

* **Python 3.x** instalado.
* **MongoDB** rodando localmente na porta padrão (`27017`).
* **Hardware:** Recomenda-se uma máquina com pelo menos **8GB de RAM** (preferencialmente mais, ou uma GPU dedicada), pois o carregamento dos modelos de 1.3 bilhões de parâmetros consome recursos significativos da memória.

## 🔧 Instalação

1.  Clone este repositório ou baixe os arquivos.
2.  Instale as dependências necessárias via pip:

```bash
pip install pymongo transformers torch