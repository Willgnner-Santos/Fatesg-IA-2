# Importação das bibliotecas necessárias
import requests # Para fazer requisições HTTP e obter dados de uma API
import pymongo # Para interagir com o banco de dados MongoDB
# Conectar ao MongoDB
# Criamos um cliente para acessar o servidor MongoDB local na porta padrão (27017)
client = pymongo.MongoClient("mongodb+srv://felipefatesg_db_user:1234@chatbot.mrcuhu0.mongodb.net/?appName=Chatbot")
# Selecionamos o banco de dados chamado "startup"
db = client["startup2"]
# Escolhemos a coleção (equivalente a uma tabela em bancos relacionais) chamada "funcionarios"
collection = db["funcionarios2"]
# URL da API que fornece dados de usuários aleatórios
# O parâmetro "results=10" indica que queremos obter 10 usuários
# O parâmetro "nat=br" faz com que os usuários sejam de nacionalidade brasileira
url = "https://randomuser.me/api/?results=10&nat=br"
# Fazemos uma requisição GET para a API e obtemos os dados no formato JSON
response = requests.get(url).json()
# Criamos uma lista para armazenar os funcionários processados antes de inseri-los no MongoDB
funcionarios2 = []
# Percorremos cada usuário retornado pela API
for user in response["results"]:
# Extraímos os dados necessários e organizamos em um dicionário
 funcionarios2.append(
    {
        "nome": f"{user['name']['first']} {user['name']['last']}", # Nome completo do funcionário
        "idade": user["dob"]["age"], # Idade
        "email": user["email"], # Endereço de e-mail
        "telefone": user["phone"], # Número de telefone
        # Definição do cargo com base na idade: abaixo de 30 anos é "Desenvolvedor", senão "Gerente"
        "cargo": "Desenvolvedor" if user["dob"]["age"] < 30 else "Gerente",
        # Definição do salário com base no cargo: Desenvolvedor recebe R$ 7.000 e Gerente recebe R$ 12.000
        "salario": 7000 if user["dob"]["age"] < 30 else 12000,
        "setor": "TI" # Setor padrão para todos os funcionários
    }
)
# Inserimos todos os funcionários processados na coleção "funcionarios" do banco de dados MongoDB
collection.insert_many(funcionarios2)
# Mensagem indicando que os dados foram inseridos com sucesso no banco de dados
print("Dados inseridos com sucesso!")