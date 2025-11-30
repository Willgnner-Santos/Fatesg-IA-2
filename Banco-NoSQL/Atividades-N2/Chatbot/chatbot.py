#CHATBOT NO MONGODB POR PABLO HENRIQUE E LUCA ATANAZIO

# ------------------------------
# 1) IMPORTAÇÕES
# ------------------------------
import pymongo
from collections import Counter
from datetime import datetime
import re
from transformers import pipeline

# Configuração de formatação para valores monetários
import locale
# Tenta configurar o locale para pt_BR. Se falhar (em alguns sistemas), usa o padrão.
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '') 


# ------------------------------
# 2) CONEXÃO COM MONGODB
# ------------------------------
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()
    print("Conexão com o MongoDB estabelecida com sucesso.")
except pymongo.errors.ServerSelectionTimeoutError:
    print("Erro: Não foi possível conectar ao MongoDB. Verifique se o servidor está ativo.")
    exit()
except Exception as e:
    print(f"Erro inesperado na conexão: {e}")
    exit()

# Banco e coleções
db = client["TT_Ifood"]
col_func = db["funcionarios"]
col_conv = db["conversas"]

# Carregar funcionários
funcionarios = list(col_func.find({}))
if not funcionarios:
    print("Coleção 'funcionarios' vazia. Popule os dados antes de continuar.")
    client.close()
    exit()
print(f"[INFO] {len(funcionarios)} funcionários carregados do MongoDB.")

# ------------------------------
# 3) ESTATÍSTICAS
# ------------------------------
# Filtra dados garantindo que sejam do tipo correto e evita divisão por zero
salarios = [f.get("salario", 0) for f in funcionarios if isinstance(f.get("salario"), (int,float)) and f.get("salario") > 0]
idades = [f.get("idade", 0) for f in funcionarios if isinstance(f.get("idade"), (int,float)) and f.get("idade") > 0]
cargos = [f.get("cargo", "") for f in funcionarios if f.get("cargo")]
setores_unicos = set(f.get("setor") for f in funcionarios if f.get("setor"))

media_salarial = sum(salarios)/len(salarios) if salarios else 0
max_salario = max(salarios) if salarios else 0
min_salario = min(salarios) if salarios else 0
idade_media = sum(idades)/len(idades) if idades else 0
cargo_mais_comum = Counter(cargos).most_common(1)[0][0] if cargos else "N/A"
total_funcionarios = len(funcionarios)


print("\n[ESTATÍSTICAS]")
print(f"Média salarial: {locale.currency(media_salarial, grouping=True)}")
print(f"Salário máximo: {locale.currency(max_salario, grouping=True)}")
print(f"Salário mínimo: {locale.currency(min_salario, grouping=True)}")
print(f"Idade média: {idade_media:.1f} anos")
print(f"Cargo mais comum: {cargo_mais_comum}")
print(f"Total de setores: {len(setores_unicos)}")

# Texto das estatísticas para contextualizar a IA
stats_text = f"""
Dados da empresa (Use estes dados para formular a pergunta):
- Total de funcionários: {total_funcionarios}
- Média salarial: {round(media_salarial,2)}
- Maior salário: {round(max_salario,2)}
- Menor salário: {round(min_salario,2)}
- Idade média: {round(idade_media,1)}
- Cargo mais comum: {cargo_mais_comum}
- Setores: {', '.join(setores_unicos)}
"""

# Armazena estatísticas chave em um dicionário para uso na função de resposta
stats_data = {
    "media_salarial": media_salarial,
    "max_salario": max_salario,
    "min_salario": min_salario,
    "idade_media": idade_media,
    "cargo_mais_comum": cargo_mais_comum,
    "total_funcionarios": total_funcionarios
}

# ------------------------------
# 4) CARREGAR MODELO OPT
# ------------------------------
print("\n[INFO] Carregando modelo facebook/opt-iml-1.3b...")
modelo = pipeline("text-generation", model="facebook/opt-iml-1.3b")
print("[OK] Modelo carregado.")

# ------------------------------
# 5) FUNÇÃO PARA GERAR PERGUNTA (IA)
# ------------------------------
def gerar_pergunta():
    """Gera uma pergunta analítica curtas usando a IA."""
    # O prompt foi ajustado para pedir uma pergunta mais "coerente" e "relevante"
    prompt = (
        "Você é um gerador de perguntas curtas em português.\n"
        "Crie uma pergunta clara e curta (máx. 12 palavras) que exija análise de AGREGADOS (média, máximo, comum) e seja a mais COERENTE e RELEVANTE possível com base nos dados a seguir.\n"
        "A pergunta deve terminar com '?'. Apenas a pergunta, sem introduções.\n\n"
        f"{stats_text}\n\n"
        "Pergunta:"
    )

    out = modelo(
        prompt,
        max_new_tokens=40,
        do_sample=True,
        top_p=0.8,
        temperature=0.7 # Aumentado para estimular mais criatividade na pergunta
    )[0]["generated_text"]

    # Limpeza de texto gerado pela IA (mantida a lógica robusta)
    pergunta = out.replace(prompt, "").strip().split("\n")[0]
    pergunta = re.sub(r'^[\s\W]*','', pergunta)
    
    if not pergunta.endswith("?"):
        pergunta = re.sub(r'[\.\:]+$', '', pergunta).strip()
        pergunta = pergunta + "?"
    
    if len(pergunta) < 10:
        return "Qual é a média salarial da empresa?" # Fallback
        
    return pergunta

# ------------------------------
# 6) FUNÇÃO PARA GERAR RESPOSTA (LÓGICA INTERNA)
# ------------------------------
def analisar_e_responder(pergunta, stats):
    """Analisa a pergunta usando palavras-chave e as estatísticas pré-calculadas."""
    pergunta_lower = pergunta.lower()
    
    # Resposta sobre o total de funcionários
    if any(keyword in pergunta_lower for keyword in ["quantos", "total de", "número de", "funcionários"]):
        return f"O total de funcionários cadastrados no sistema é de {stats['total_funcionarios']}."

    # Resposta sobre média salarial
    if "média salarial" in pergunta_lower or "salário médio" in pergunta_lower:
        return f"A média salarial da empresa é de {locale.currency(stats['media_salarial'], grouping=True)}."
    
    # Resposta sobre salário máximo/mínimo
    if "máximo salário" in pergunta_lower or "salário máximo" in pergunta_lower:
        return f"O salário máximo registrado é de {locale.currency(stats['max_salario'], grouping=True)}."
    if "mínimo salário" in pergunta_lower or "salário mínimo" in pergunta_lower:
        return f"O salário mínimo registrado é de {locale.currency(stats['min_salario'], grouping=True)}."
        
    # Resposta sobre o cargo mais comum
    if "cargo mais comum" in pergunta_lower or "mais pessoas" in pergunta_lower:
        return f"O cargo mais comum na empresa é: {stats['cargo_mais_comum']}."
    
    # Resposta sobre idade média
    if "média de idade" in pergunta_lower or "idade média" in pergunta_lower:
        return f"A idade média dos funcionários é de {stats['idade_media']:.1f} anos."

    # Resposta para perguntas mais complexas (como por setor)
    return "Esta pergunta requer uma análise de agregação por grupo (ex: setor, cargo) que o chatbot não pode realizar diretamente. As estatísticas globais estão disponíveis."

# ------------------------------
# 7) FLUXO AUTOMÁTICO DE GERAÇÃO E REGISTRO
# ------------------------------
print("\n=== FLUXO AUTOMÁTICO (GERAÇÃO DE PERGUNTA EM LOTE) ===")

# 1. Geração da pergunta pela IA
pergunta_gerada = gerar_pergunta()

# 2. Geração da resposta pela lógica interna
resposta_analitica = analisar_e_responder(pergunta_gerada, stats_data)

# 3. Exibição e Registro
print(f"\n[PERGUNTA GERADA]: {pergunta_gerada}")
print(f"[RESPOSTA ANALÍTICA]: {resposta_analitica}")

try:
    col_conv.insert_one({
        "tipo": "Pergunta Gerada Automaticamente",
        "pergunta": pergunta_gerada,
        "resposta": resposta_analitica,
        "modelo_resposta": "Lógica Interna (Estatísticas)",
        "timestamp": datetime.now()
    })
    print("\n[OK] Pergunta e Resposta salvas no MongoDB.")
except Exception as e:
    print(f"\n[ERRO] Falha ao salvar no MongoDB: {e}")

# Fechar a conexão com o MongoDB
client.close()
print("Conexão com o MongoDB fechada. Script encerrado.")