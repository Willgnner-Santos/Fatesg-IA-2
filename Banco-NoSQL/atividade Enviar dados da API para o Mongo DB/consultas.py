from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
col = client['startup']['funcionarios']

print("Funcionários setor TI:")
for doc in col.find({"setor": "TI"}):
    print(doc)

print("\nFuncionários com salário maior que 10.000:")
for doc in col.find({"salario": {"$gt": 10000}}):
    print(doc)

print("\nSó gerentes:")
for doc in col.find({"cargo": "Gerente"}):
    print(doc)

print("\nNome e email:")
for doc in col.find({}, {"_id":0, "nome":1, "email":1}):
    print(doc)

print("\nIdade entre 25 e 35:")
for doc in col.find({"idade": {"$gte": 25, "$lte": 35}}):
    print(doc)
