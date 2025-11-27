# Projeto de Integração Python e MongoDB - Gestão de Funcionários

Este projeto consiste em um script Python desenvolvido em Jupyter Notebook que simula um sistema de RH para uma Startup. Ele consome dados de uma API pública, aplica regras de negócio para definição de cargos e salários, armazena as informações em um banco de dados **MongoDB** e realiza diversas operações de consulta, agregação e otimização por índices.

## 📋 Funcionalidades

O projeto abrange as seguintes etapas:

1.  **ETL (Extract, Transform, Load):**
    * **Extração:** Coleta dados de usuários aleatórios brasileiros via API `randomuser.me`.
    * **Transformação:** Define automaticamente o cargo e o salário com base na idade:
        * *< 30 anos:* Cargo "Desenvolvedor" (Salário R$ 7.000).
        * *>= 30 anos:* Cargo "Gerente" (Salário R$ 12.000).
    * **Carga:** Insere os dados processados na coleção `funcionarios` do banco `startup`.
2.  **Consultas (Queries):** Filtros simples e projeções de dados.
3.  **Aggregation Framework:** Análise de dados estatísticos (contagens, médias, máximos e somas).
4.  **Otimização:** Criação de índices simples, compostos, de texto e únicos.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **MongoDB** (Banco de dados NoSQL)
* **PyMongo** (Driver oficial do MongoDB para Python)
* **Requests** (Biblioteca para requisições HTTP)
* **Jupyter Notebook**

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de ter o Python instalado e o servidor MongoDB rodando localmente na porta padrão (`27017`).

### Instalação das Dependências

Execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install pymongo requests