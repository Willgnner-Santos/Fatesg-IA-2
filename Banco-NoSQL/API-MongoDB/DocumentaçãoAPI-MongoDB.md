# Documentação - Integração de API REST com MongoDB

## Objetivo
Esta Documentação demonstra como consumir dados de uma API REST externa (RandomUser) e armazená-los em um banco de dados MongoDB, além de realizar consultas básicas, agregações e configuração de índices.

## Ambiente de Desenvolvimento
- **Sistema Operacional**: Arch Linux
- **Editor**: Visual Studio Code
- **MongoDB**: Executado via Docker
- **Interface Gráfica**: MongoDB Compass
- **Python**: Ambiente virtual (venv)

## Preparação do Ambiente

### 1. Configuração do MongoDB via Docker
```bash
# Download e execução do container MongoDB
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 2. Instalação do MongoDB Compass
```bash
# Instalação no Arch Linux
sudo pacman -S mongodb-compass
```

### 3. Dependências Python
```bash
# Ativação do ambiente virtual
source venv_mongodb/bin/activate

# Instalação das bibliotecas necessárias
pip install requests pymongo
```

## Código Principal

### Script de Integração (API-mongo.py)

```python
# Importação das bibliotecas necessárias
import requests  # Para fazer requisições HTTP e obter dados de uma API
import pymongo   # Para interagir com o banco de dados MongoDB

# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["startup"]
collection = db["funcionarios"]

# URL da API que fornece dados de usuários aleatórios
url = "https://randomuser.me/api/?results=10&nat=br"

# Fazemos uma requisição GET para a API e obtemos os dados no formato JSON
response = requests.get(url).json()

# Lista para armazenar os funcionários processados
funcionarios = []

# Processar cada usuário retornado pela API
for user in response["results"]:
    funcionarios.append({
        "nome": f"{user['name']['first']} {user['name']['last']}",
        "idade": user["dob"]["age"],
        "email": user["email"],
        "telefone": user["phone"],
        "cargo": "Desenvolvedor" if user["dob"]["age"] < 30 else "Gerente",
        "salario": 7000 if user["dob"]["age"] < 30 else 12000,
        "setor": "TI"
    })

# Inserir todos os funcionários no MongoDB
collection.insert_many(funcionarios)
print("Dados inseridos com sucesso!")
```

## Execução do Script

### Resultado da Execução
```bash
(venv_mongodb) [MiguelAl@arch API-MongoDB]$ python API-mongo.py
Dados inseridos com sucesso!
```

**Dados processados:**
- 20 funcionários inseridos na coleção
- Dados brasileiros obtidos da API RandomUser
- Processamento automático de cargos baseado na idade
- Salários definidos por regra de negócio

## Estrutura dos Dados no MongoDB

### Campos Armazenados
| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| _id | ObjectId | Identificador único do MongoDB | ObjectId('68d410efd769b5c...') |
| nome | String | Nome completo do funcionário | "Iolanda Nascimento" |
| idade | Int32 | Idade em anos | 79 |
| email | String | Endereço de e-mail | "iolanda.nascimento@example.com" |
| telefone | String | Número de telefone | "(80) 0207-7478" |
| cargo | String | Cargo na empresa | "Gerente" ou "Desenvolvedor" |
| salario | Int32 | Salário em reais | 12000 ou 7000 |
| setor | String | Setor de trabalho | "TI" |

### Regras de Negócio Aplicadas
- **Idade < 30**: Cargo "Desenvolvedor", Salário R$ 7.000
- **Idade ≥ 30**: Cargo "Gerente", Salário R$ 12.000
- **Setor**: Todos os funcionários no setor "TI"

## Consultas Realizadas via MongoDB Compass

### 1. Buscar Funcionários do Setor TI
```json
{"setor": "TI"}
```
**Resultado:** 20 documentos retornados (todos os funcionários)

### 2. Funcionários com Salário > R$ 10.000
```json
{"salario": {"$gt": 10000}}
```
**Resultado:** 18 funcionários (apenas Gerentes)

### 3. Buscar Apenas Gerentes
```json
{"cargo": "Gerente"}
```
**Resultado:** 18 funcionários com cargo de Gerente

### 4. Projeção de Nome e Email
```json
// Query
{}
// Project
{"_id": 0, "nome": 1, "email": 1}
```
**Resultado:** Lista simplificada com apenas nomes e e-mails

### 5. Funcionários entre 25 e 35 Anos
```json
{"idade": {"$gte": 25, "$lte": 35}}
```
**Resultado:** 2 funcionários na faixa etária especificada

## Agregações (Pipeline de Agregação)

### 1. Contagem de Funcionários por Cargo
```json
[
  {
    "$group": {
      "_id": "$cargo",
      "total_funcionarios": {"$sum": 1}
    }
  }
]
```
**Resultado:**
- Gerente: 18 funcionários
- Desenvolvedor: 2 funcionários

### 2. Média Salarial por Setor
```json
[
  {
    "$group": {
      "_id": "$setor",
      "media_salarial": {"$avg": "$salario"}
    }
  }
]
```
**Resultado:**
- TI: R$ 11.500 (média salarial)

### 3. Maior Idade por Setor
```json
[
  {
    "$group": {
      "_id": "$setor",
      "maior_idade": {"$max": "$idade"}
    }
  }
]
```
**Resultado:**
- TI: 79 anos (funcionário mais velho)

### 4. Lista de Funcionários por Setor
```json
[
  {
    "$group": {
      "_id": "$setor",
      "nomes": {"$push": "$nome"}
    }
  }
]
```
**Resultado:** Array com todos os 20 nomes dos funcionários

### 5. Soma Total de Salários por Cargo
```json
[
  {
    "$group": {
      "_id": "$cargo",
      "total_salario": {"$sum": "$salario"}
    }
  }
]
```
**Resultado:**
- Desenvolvedor: R$ 14.000 (2 × R$ 7.000)
- Gerente: R$ 216.000 (18 × R$ 12.000)

## Configuração de Índices

### Índices Criados Automaticamente
O MongoDB Compass mostra 4 índices configurados:

1. **_id_ (REGULAR)** - Índice único padrão
   - Tamanho: 36.9 KB
   - Propriedade: UNIQUE
   - Status: READY

2. **nome_text (TEXT)** - Índice de texto para busca
   - Tamanho: 20.5 KB
   - Uso: Busca textual em nomes
   - Status: READY

3. **salario_1 (REGULAR)** - Índice numérico para salários
   - Tamanho: 20.5 KB
   - Uso: Consultas por faixa salarial
   - Status: READY

4. **email_1 (REGULAR)** - Índice único para e-mails
   - Tamanho: 20.5 KB
   - Propriedade: UNIQUE
   - Status: READY

### Tipos de Índices Utilizados

#### Índice de Texto
```json
{"nome": "text"}
```
**Utilização:**
```json
{"$text": {"$search": "Iolanda"}}
```

#### Índice Numérico
```json
{"salario": 1}
```
**Utilização:**
```json
{"salario": {"$gte": 10000}}
```

#### Índice Único
```json
{"email": 1, "unique": true}
```
**Utilização:** Previne e-mails duplicados

## Validação de Schema

### Schema de Validação Aplicado
```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["nome", "idade", "email", "cargo", "salario", "setor"],
    "properties": {
      "nome": {
        "bsonType": "string",
        "description": "O nome deve ser uma string."
      },
      "idade": {
        "bsonType": "int",
        "minimum": 18,
        "description": "A idade deve ser um número inteiro maior ou igual a 18."
      },
      "email": {
        "bsonType": "string",
        "pattern": "^.+@.+\..+$",
        "description": "O email deve ser um endereço válido."
      },
      "cargo": {
        "bsonType": "string",
        "enum": ["Desenvolvedor", "Gerente"],
        "description": "O cargo deve ser 'Desenvolvedor' ou 'Gerente'."
      },
      "salario": {
        "bsonType": "int",
        "minimum": 0,
        "description": "O salário deve ser um número inteiro positivo."
      },
      "setor": {
        "bsonType": "string",
        "description": "O setor deve ser uma string."
      }
    }
  }
}
```

### Regras de Validação
- **Campos obrigatórios:** nome, idade, email, cargo, salario, setor
- **Idade mínima:** 18 anos
- **Email:** Formato válido com @
- **Cargo:** Apenas "Desenvolvedor" ou "Gerente"
- **Salário:** Valor positivo

## Análise dos Dados Obtidos

### Distribuição por Cargo
- **Gerentes:** 18 funcionários (90%)
- **Desenvolvedores:** 2 funcionários (10%)

### Distribuição por Faixa Etária
- **Abaixo de 30 anos:** 2 funcionários
- **30 anos ou mais:** 18 funcionários

### Análise Salarial
- **Massa salarial total:** R$ 230.000
- **Salário médio:** R$ 11.500
- **Maior concentração:** Gerentes (R$ 12.000)

## Interface MongoDB Compass

### Funcionalidades Utilizadas

1. **Documents (20)** - Visualização dos documentos
2. **Aggregations** - Pipeline de agregação visual
3. **Schema** - Análise da estrutura dos dados
4. **Indexes (4)** - Gerenciamento de índices
5. **Validation** - Configuração de regras de validação

### Operações Realizadas
- ✅ **Consultas simples** com filtros
- ✅ **Agregações complexas** com múltiplos estágios
- ✅ **Criação de índices** para otimização
- ✅ **Validação de schema** para integridade
- ✅ **Projeções** para campos específicos

## Vantagens da Solução

### MongoDB
- **Flexibilidade:** Schema dinâmico permite adaptações
- **Performance:** Índices otimizam consultas
- **Agregações:** Pipeline poderoso para análise
- **Escalabilidade:** Suporte a grandes volumes

### API Integration
- **Dados reais:** RandomUser fornece dados consistentes
- **Automação:** Processamento automático de regras de negócio
- **Flexibilidade:** Fácil adaptação para outras APIs

## Casos de Uso Demonstrados

### 1. Importação de Dados Externos
- Consumo de API REST
- Transformação de dados
- Inserção em lote no MongoDB

### 2. Análise de Dados
- Consultas por critérios específicos
- Agregações para insights
- Projeções para relatórios

### 3. Otimização de Performance
- Índices para consultas frequentes
- Validação para integridade
- Estruturação adequada dos dados

## Conclusão

O projeto estabelece uma base sólida para sistemas de integração de dados em tempo real, demonstrando as capacidades do MongoDB como banco NoSQL para aplicações modernas.
Nossa... esse deu trabalho
