# --- ETAPA 2: IA GERANDO PERGUNTAS SOBRE DADOS ---

# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ---------------------------------------------------------------------
import pymongo  # O "conector" que permite ao Python conversar com o MongoDB.
from transformers import pipeline  # A "fábrica" de modelos de IA do Hugging Face.


# 2. CONEXÃO COM O BANCO DE DADOS MONGODB
# ---------------------------------------------------------------------


client = pymongo.MongoClient("mongodb://localhost:27017/")
# Cria a conexão com o servidor do MongoDB que está rodando na sua máquina.

db = client["chatbot"]


collection = db["perguntas_analiticas"]


# 3. CARREGAMENTO DO MODELO DE IA (O CÉREBRO INSTRUCIONAL)
# ---------------------------------------------------------------------

print("Carregando o modelo 'facebook/opt-iml-1.3b'...")
# Isso pode demorar alguns minutos na primeira vez, pois ele precisa baixar
# os bilhões de parâmetros do modelo.


modelo_analista = pipeline(
    "text-generation",                  
    model="facebook/opt-iml-1.3b"       
)

print("Modelo carregado com sucesso!")

# 4. CRIAÇÃO DO PROMPT (REFINADO E ESPECÍFICO)
# ---------------------------------------------------------------------

# Mudamos o prompt para evitar que ele fale de viagens.
# Damos exemplos curtos para ele seguir o padrão curto.
prompt_para_ia = """Lista de 15 perguntas analíticas de RH sobre dados de funcionários, salários e departamentos:

1. Qual a média de idade dos funcionários?
2. Qual departamento tem o maior salário médio?
3. Quantos funcionários trabalham em cada cargo?
4. Qual é o salário mais alto da empresa?
5. Qual é o tempo médio de casa dos funcionários?
6.""" 

# 5. EXECUÇÃO DA IA
# ---------------------------------------------------------------------

print("Gerando perguntas analíticas focadas...")

resultado = modelo_analista(
    prompt_para_ia,
    max_length=250,         
    do_sample=True,
    temperature=0.3,         
    repetition_penalty=1.05, 
    num_return_sequences=1
)

texto_completo = resultado[0]["generated_text"]

# --- LIMPEZA E FORMATAÇÃO ---

# 1. Tenta cortar na pergunta 16 para fechar a lista
if "16." in texto_completo:
    perguntas_finais = texto_completo.split("16.")[0]
else:
    perguntas_finais = texto_completo

perguntas_finais = perguntas_finais.strip()

# 6. ARMAZENAMENTO NO MONGODB
# ---------------------------------------------------------------------

documento_salvo = {
    "prompt_enviado": prompt_para_ia,
    "perguntas_geradas": perguntas_finais
}

collection.insert_one(documento_salvo)

print("Perguntas geradas e armazenadas com sucesso no MongoDB!")

print("\n--- RESULTADO FINAL ---")
print(perguntas_finais)

# Verifica visualmente se ele gerou 15 linhas numeradas
linhas = perguntas_finais.split('\n')
print(f"\nTotal de linhas geradas: {len(linhas)}")