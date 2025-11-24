import pymongo
from transformers import pipeline

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]
collection = db["conversas"]

modelo = pipeline("text-generation", model="facebook/opt-1.3b")

# Exemplo inicial de pergunta
pergunta = input("Qual sua pergunta? \n")

resposta = modelo(pergunta, max_length=100, do_sample=True)[0]["generated_text"]

collection.insert_one({
    "pergunta": pergunta,
    "resposta": resposta
})

#print("Resposta armazenada com sucesso!")
#pythonprint("Pergunta:", pergunta)
print("Resposta:", resposta)
