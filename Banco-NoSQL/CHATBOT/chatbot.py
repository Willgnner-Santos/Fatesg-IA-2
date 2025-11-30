import pymongo
from transformers import pipeline
import re

try:
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError:
    print("Erro: Não foi possível conectar ao MongoDB.")
    exit()

db = client["startup"]
collection = db["conversas"]


print("Carregando modelo de IA, isso pode levar alguns minutos...")
modelo = pipeline("text-generation", model="facebook/opt-1.3b")

def calcular_score(frase1, frase2):
    f1 = set(re.sub(r"[^a-zA-Z0-9áéíóúâêôãõç ]", "", frase1.lower()).split())
    f2 = set(re.sub(r"[^a-zA-Z0-9áéíóúâêôãõç ]", "", frase2.lower()).split())

    if not f1 or not f2:
        return 0

    inter = f1.intersection(f2)
    score = len(inter) / max(len(f1), len(f2))

    return score

def buscar_no_banco(pergunta_usuario):
    todas = list(collection.find({}))

    melhor_score = 0
    melhor_resposta = None

    for conv in todas:
        score = calcular_score(pergunta_usuario, conv["pergunta"])

        if score > melhor_score:
            melhor_score = score
            melhor_resposta = conv["resposta"]

    if melhor_score > 0.35:
        return melhor_resposta
    
    return None

def gerar_ia(pergunta_texto):
    resposta = modelo(pergunta_texto, max_length=120, do_sample=True)[0]["generated_text"]
    return resposta

def processar_pergunta(pergunta_texto):

    resposta_banco = buscar_no_banco(pergunta_texto)

    if resposta_banco:
        resposta = resposta_banco
        origem = "banco"   
    else:
        resposta = gerar_ia(pergunta_texto)
        origem = "ia"

    collection.insert_one({
        "pergunta": pergunta_texto,
        "resposta": resposta
    })

    return resposta, origem

print("\n=== Chatbot IA + MongoDB ===")
print("Digite sua pergunta.")
print("Para sair: sair / exit\n")

while True:
    pergunta_usuario = input("Você: ")
    
    if pergunta_usuario.lower() in ["sair", "exit"]:
        print("Encerrando chatbot...")
        break

    resposta, origem = processar_pergunta(pergunta_usuario)

    print(f"Chatbot ({'MongoDB' if origem=='banco' else 'IA'}):", resposta)

print("\n--- Histórico armazenado ---")

for idx, conversa in enumerate(collection.find(), 1):
    print(f"\nConversa {idx}:")
    print("Pergunta:", conversa["pergunta"])
    print("Resposta:", conversa["resposta"])

print("\nChatbot finalizado!")