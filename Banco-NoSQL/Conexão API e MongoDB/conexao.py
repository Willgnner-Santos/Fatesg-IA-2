import requests  
import pymongo 

client = pymongo.MongoClient("mongodb://localhost:27017/") 
db = client["startup"] 
collection = db["funcionarios"] 

url = "https://randomuser.me/api/?results=10&nat=br" 

response = requests.get(url).json() 


funcionarios = [] 


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

collection.insert_many(funcionarios) 

print("Dados inseridos com sucesso!") 