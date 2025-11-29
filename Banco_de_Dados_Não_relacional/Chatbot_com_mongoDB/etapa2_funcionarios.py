import pymongo
from transformers import pipeline

print("--- INICIANDO ETAPA 2: ANÁLISE DE FUNCIONÁRIOS ---")

# 1. CONEXÃO COM O MONGODB
# ---------------------------------------------------------
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["chatbot"]
    col_funcionarios = db["funcionarios"]
    col_conversas = db["conversas"]
    print("Conexão com MongoDB realizada com sucesso.")
except Exception as e:
    print(f"Erro ao conectar: {e}")
    exit()

# 2. INSERÇÃO DE DADOS FICTÍCIOS (POPULAR O BANCO)
# ---------------------------------------------------------
# Verificamos se a coleção já tem dados para não duplicar toda vez que rodar
if col_funcionarios.count_documents({}) == 0:
    print("Inserindo dados fictícios de funcionários...")
    lista_funcionarios = [
        {"nome": "Ana Silva", "cargo": "Analista de Dados", "idade": 29, "salario": 5500},
        {"nome": "Carlos Souza", "cargo": "Desenvolvedor Backend", "idade": 35, "salario": 7000},
        {"nome": "Beatriz Lima", "cargo": "Gerente de Projetos", "idade": 42, "salario": 12000},
        {"nome": "João Mendes", "cargo": "Estagiário", "idade": 22, "salario": 1800},
        {"nome": "Fernanda Torres", "cargo": "Desenvolvedora Frontend", "idade": 27, "salario": 6000}
    ]
    col_funcionarios.insert_many(lista_funcionarios)
    print(f"{len(lista_funcionarios)} funcionários inseridos com sucesso!")
else:
    print("A coleção 'funcionarios' já contém dados. Pulando inserção.")

# 3. CARREGAMENTO DO MODELO DE IA (Hugging Face)
# ---------------------------------------------------------
print("Carregando o modelo 'facebook/opt-iml-1.3b'. Aguarde, isso pode demorar...")

try:
    gerador = pipeline("text-generation", model="facebook/opt-iml-1.3b")
except Exception as e:
    print(f"Erro ao carregar o modelo. Verifique sua conexão ou memória. Detalhe: {e}")
    exit()

# 4. DEFINIÇÃO DO PROMPT (CONTEXTO)
# ---------------------------------------------------------
# Aqui explicamos para a IA o que temos no banco e pedimos para ela criar perguntas.
contexto = (
    "Abaixo está o esquema de um banco de dados de funcionários:\n"
    "Colunas: Nome, Cargo, Idade, Salario.\n"
    "Tarefa: Gere 3 perguntas analíticas em português para extrair insights desses dados.\n"
    "Perguntas:"
)

# 5. GERAÇÃO DA RESPOSTA
# ---------------------------------------------------------
print("Gerando perguntas com a IA...")
# Adicionamos 'repetition_penalty=1.2' para evitar loops e 'temperature=0.7' para ser mais criativo
resultado = gerador(contexto, max_length=100, do_sample=True, repetition_penalty=1.2, temperature=0.7)[0]["generated_text"]

# Limpeza: Removemos o prompt original para ficar apenas com as perguntas geradas
perguntas_geradas = resultado.replace(contexto, "").strip()

# 6. ARMAZENAMENTO E EXIBIÇÃO
# ---------------------------------------------------------
# Salvamos na coleção de conversas para evidenciar o teste
doc_interacao = {
    "prompt_enviado": contexto,
    "resposta_ia": perguntas_geradas
}
col_conversas.insert_one(doc_interacao)

print("\n" + "="*40)
print("RESPOSTA DA IA (PERGUNTAS SUGERIDAS):")
print("="*40)
print(perguntas_geradas)
print("="*40)
print("Interação salva na coleção 'conversas' e dados de funcionários verificados.")