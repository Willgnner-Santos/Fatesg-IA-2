import pymongo
import random

# --- Configuração ---
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["startup"]
collection = db['funcionarios']

# 1. Limpar a coleção antes de inserir (opcional, para evitar duplicação em testes)
collection.drop()
print("Coleção antiga limpa.")

# Lista para armazenar os documentos
novos_funcionarios = []

# 2. Gerar 100 registros fictícios
for _ in range(100):
    # Idade aleatória entre 18 e 65 anos
    idade = random.randint(18, 65)
    
    # Lógica do Salário (Simulando a realidade):
    # Salário Base (R$ 1.500) + (R$ 120 por ano de idade) + Variação (Sorte/Azar de +/- R$ 1000)
    # Isso garante que existe uma TENDÊNCIA de alta, mas não é uma linha reta perfeita.
    salario_base = 1500
    fator_experiencia = 120 * (idade - 18) # Paga mais por anos acima de 18
    ruido_aleatorio = random.uniform(-800, 800) # Variação para o modelo não ficar viciado
    
    salario_final = salario_base + fator_experiencia + ruido_aleatorio
    
    # Garantir que ninguém ganhe menos que o salário mínimo (só por segurança)
    if salario_final < 1412:
        salario_final = 1412

    doc = {
        "nome": f"Funcionario_{random.randint(1000, 9999)}", # Nome fictício
        "idade": int(idade),
        "salario": round(salario_final, 2),
        "cargo": random.choice(["Dev", "Analista", "Gerente", "Estagiário"]) # Só para constar
    }
    
    novos_funcionarios.append(doc)

# 3. Inserir no MongoDB de uma vez (Bulk Insert é mais rápido)
collection.insert_many(novos_funcionarios)

print(f"Sucesso! {len(novos_funcionarios)} funcionários inseridos no banco 'startup'.")
print("Agora você pode rodar seu script de Regressão Linear.")