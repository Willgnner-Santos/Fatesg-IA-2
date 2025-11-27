# Importação das bibliotecas necessárias
import requests  # Para fazer requisições HTTP e obter dados de uma API
import pymongo   # Para interagir com o banco de dados MongoDB

# Conectar ao MongoDB
# Criamos um cliente para acessar o servidor MongoDB local na porta padrão (27017)
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Selecionamos o banco de dados chamado "startup"
db = client["startup"]

# Escolhemos a coleção (equivalente a uma tabela em bancos relacionais) chamada "funcionarios"
collection = db["funcionarios"]

# URL da API que fornece dados de usuários aleatórios
# O parâmetro "results=10" indica que queremos obter 10 usuários
# O parâmetro "nat=br" faz com que os usuários sejam de nacionalidade brasileira
url = "https://randomuser.me/api/?results=10&nat=br"

# Fazemos uma requisição GET para a API e obtemos os dados no formato JSON
response = requests.get(url).json()

# Criamos uma lista para armazenar os funcionários processados antes de inseri-los no MongoDB
funcionarios = []

# Percorremos cada usuário retornado pela API
for user in response["results"]:
    # Extraímos os dados necessários e organizamos em um dicionário
    funcionarios.append({
        "nome": f"{user['name']['first']} {user['name']['last']}",  # Nome completo do funcionário
        "idade": user["dob"]["age"],                                   # Idade
        "email": user["email"],                                        # Endereço de e-mail
        "telefone": user["phone"],                                     # Número de telefone
        # Definição do cargo com base na idade: abaixo de 30 anos é "Desenvolvedor", senão "Gerente"
        "cargo": "Desenvolvedor" if user["dob"]["age"] < 30 else "Gerente",
        # Definição do salário com base no cargo: Desenvolvedor recebe R$ 7.000 e Gerente recebe R$ 12.000
        "salario": 7000 if user["dob"]["age"] < 30 else 12000,
        "setor": "TI"  # Setor padrão para todos os funcionários
    })

# Inserimos todos os funcionários processados na coleção "funcionarios" do banco de dados MongoDB
collection.insert_many(funcionarios)

# Mensagem indicando que os dados foram inseridos com sucesso no banco de dados
print("Dados inseridos com sucesso!")

# ============================= CONSULTAS NOS DADOS =============================

# 1. Consulta: Listar todos os funcionários
print("\n--- TODOS OS FUNCIONÁRIOS ---")
todos = collection.find()
for funcionario in todos:
    print(f"Nome: {funcionario['nome']} | Cargo: {funcionario['cargo']} | Salário: R$ {funcionario['salario']}")

# 2. Consulta: Listar apenas os Desenvolvedores
print("\n--- DESENVOLVEDORES ---")
desenvolvedores = collection.find({"cargo": "Desenvolvedor"})
for dev in desenvolvedores:
    print(f"Nome: {dev['nome']} | Idade: {dev['idade']} | Email: {dev.get('email', 'N/A')}")

# 3. Consulta: Listar apenas os Gerentes
print("\n--- GERENTES ---")
gerentes = collection.find({"cargo": "Gerente"})
for gerente in gerentes:
    print(f"Nome: {gerente['nome']} | Idade: {gerente['idade']} | Email: {gerente.get('email', 'N/A')}")

# 4. Consulta: Contar quantos funcionários existem por cargo
print("\n--- CONTAGEM POR CARGO ---")
total_devs = collection.count_documents({"cargo": "Desenvolvedor"})
total_gerentes = collection.count_documents({"cargo": "Gerente"})
print(f"Total de Desenvolvedores: {total_devs}")
print(f"Total de Gerentes: {total_gerentes}")

# 5. Consulta: Calcular a folha de pagamento total
print("\n--- FOLHA DE PAGAMENTO ---")
todos = collection.find()
folha_total = sum(func['salario'] for func in todos)
print(f"Folha de pagamento total: R$ {folha_total:,}")

# 6. Consulta: Funcionários com idade maior que 35 anos
print("\n--- FUNCIONÁRIOS COM MAIS DE 35 ANOS ---")
maiores_35 = collection.find({"idade": {"$gt": 35}})
for func in maiores_35:
    print(f"Nome: {func['nome']} | Idade: {func['idade']} | Cargo: {func['cargo']}")

# 7. Consulta: Buscar funcionário por nome específico
print("\n--- BUSCAR POR NOME ---")
nome_busca = collection.find_one({"nome": {"$regex": "", "$options": "i"}})  # Busca case-insensitive
if nome_busca:
    print(f"Encontrado: {nome_busca['nome']} | {nome_busca.get('email', 'N/A')}")
else:
    print("Funcionário não encontrado")

# 8. Consulta: Ordenar funcionários por salário (decrescente)
print("\n--- FUNCIONÁRIOS ORDENADOS POR SALÁRIO (MAIOR PARA MENOR) ---")
por_salario = collection.find().sort("salario", -1)
for func in por_salario:
    print(f"Nome: {func['nome']} | Salário: R$ {func['salario']}")

# 9. Consulta: Média de idade
print("\n--- MÉDIA DE IDADE ---")
todos = collection.find()
idades = [func['idade'] for func in todos]
media_idade = sum(idades) / len(idades) if idades else 0
print(f"Média de idade: {media_idade:.1f} anos")

# 10. Consulta: Funcionários do setor TI
print("\n--- FUNCIONÁRIOS DO SETOR TI ---")
ti = collection.find({"setor": "TI"})
for func in ti:
    print(f"Nome: {func['nome']} | Telefone: {func.get('telefone', 'N/A')}")