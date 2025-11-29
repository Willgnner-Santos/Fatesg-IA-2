# GERADOR DE 1.000 FUNCIONÁRIOS BRASILEIROS PARA MONGODB (VERSÃO CORRIGIDA)
# ------------------------------------------------------------

import pymongo
import random
import time

# ------------------------------------------------------------
# 1. CONECTAR AO MONGODB (com tratamento de erro)
# ------------------------------------------------------------
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()  # força verificação de conexão
except Exception as e:
    print("Erro: Não foi possível conectar ao MongoDB.")
    print("Detalhe:", e)
    raise SystemExit(1)

db = client["TT_Ifood"]
collection = db["funcionarios"]

# ------------------------------------------------------------
# 2. LISTAS DE NOMES, SOBRENOMES E CARGOS
# ------------------------------------------------------------
nomes = [
    "João", "Maria", "Pedro", "Ana", "Lucas", "Julia", "Marcos", "Beatriz", "Felipe",
    "Larissa", "Gabriel", "Patrícia", "André", "Carolina", "Rafael", "Camila", "Rodrigo",
    "Daniela", "Gustavo", "Aline", "Diego", "Letícia", "Thiago", "Renata"
]

sobrenomes = [
    "Silva", "Souza", "Costa", "Santos", "Oliveira", "Pereira", "Rodrigues", "Almeida",
    "Nascimento", "Lima", "Araujo", "Fernandes", "Carvalho", "Gomes", "Martins", "Ribeiro",
    "Barbosa", "Cardoso", "Melo", "Dias", "Rocha"
]

cargos_ti = {
    "Desenvolvedor Júnior": (7000, 15000),
    "Desenvolvedor Pleno": (15000, 28000),
    "Desenvolvedor Sênior": (28000, 40000),
    "Analista de Dados Júnior": (7000, 15000),
    "Analista de Dados Pleno": (15000, 28000),
    "Analista de Dados Sênior": (28000, 40000),
    "Engenheiro de Software": (20000, 38000),
    "Cientista de Dados": (25000, 40000),
    "Arquiteto de Software": (30000, 40000),
    "Coordenador de TI": (30000, 40000),
    "Arquiteto de Dados": (18000, 35000),
    "Engenheiro de Machine Learning": (15000, 28000)
}

# ------------------------------------------------------------
# 3. FUNÇÃO PARA GERAR IDADES REALISTAS DEPENDENDO DO CARGO
# ------------------------------------------------------------
def gerar_idade_por_cargo(cargo):
    # garante intervalo final 18..65
    # JUNIOR — maioria entre 20 e 30, alguns entre 18 e 35
    if "Júnior" in cargo:
        if random.random() < 0.75:
            idade = random.randint(20, 30)
        else:
            idade = random.randint(18, 35)
    # PLENO — maioria entre 28 e 40, alguns 25–45
    elif "Pleno" in cargo:
        if random.random() < 0.70:
            idade = random.randint(28, 40)
        else:
            idade = random.randint(25, 45)
    # SÊNIOR / ARQUITETO — maioria entre 35 e 55, alguns 30–60
    elif "Sênior" in cargo or "Arquiteto" in cargo:
        if random.random() < 0.70:
            idade = random.randint(35, 55)
        else:
            idade = random.randint(30, 60)
    # COORDENADOR — maioria entre 35–60
    elif "Coordenador" in cargo:
        if random.random() < 0.80:
            idade = random.randint(35, 55)
        else:
            idade = random.randint(30, 65)
    # CIENTISTA / ML / ENGENHEIRO — variação 28–45 principalmente
    elif "Cientista" in cargo or "Machine" in cargo or "Engenheiro" in cargo:
        if random.random() < 0.65:
            idade = random.randint(28, 45)
        else:
            idade = random.randint(25, 55)
    # fallback
    else:
        idade = random.randint(25, 50)

    # garantir limites 18..65
    idade = max(18, min(65, idade))
    return idade

# ------------------------------------------------------------
# 4. FUNÇÕES AUXILIARES PARA AUMENTAR VARIEDADE DE NOMES
# ------------------------------------------------------------
meios = ["", "Luiz", "Paulo", "Carlos", "Mariana", "Sofia", "Eduardo", "Mateus", "Isabela"]

def gerar_nome_completo():
    """
    Gera combinação variável:
    - às vezes inclui meio-nome
    - às vezes inclui sobrenome simples ou duplo (ex: Silva Pereira)
    Isso amplia bastante o espaço de combinações.
    """
    primeiro = random.choice(nomes)
    # 30% chance de ter meio-nome
    meio = random.choice(meios) if random.random() < 0.30 else ""
    # 40% chance de ter sobrenome duplo
    if random.random() < 0.40:
        s1 = random.choice(sobrenomes)
        s2 = random.choice(sobrenomes)
        # evitar s1 == s2
        if s1 == s2:
            s2 = random.choice([s for s in sobrenomes if s != s1])
        sobrenome = f"{s1} {s2}"
    else:
        sobrenome = random.choice(sobrenomes)

    if meio:
        nome_completo = f"{primeiro} {meio} {sobrenome}"
    else:
        nome_completo = f"{primeiro} {sobrenome}"
    # normaliza espaços duplos
    return " ".join(nome_completo.split())

# ------------------------------------------------------------
# 5. GERAR 1.000 REGISTROS (com fallback se esgotarem combinações únicas)
# ------------------------------------------------------------
funcionarios = []
combinacoes_usadas = set()
tentativas = 0
max_tentativas = 200000  # evita loop infinito absoluto

while len(funcionarios) < 1000 and tentativas < max_tentativas:
    tentativas += 1

    nome_completo = gerar_nome_completo()

    # Evitar duplicatas exatas até que tenhamos espaço; se já esgotamos combos, aceitamos duplicatas controladas
    if nome_completo in combinacoes_usadas:
        # se já temos muitas combinações únicas (ex: >900), permitimos repetir
        if len(combinacoes_usadas) < 900:
            continue
        # se já tentamos muito e não gera novo, ainda assim aceitamos repetir
    else:
        combinacoes_usadas.add(nome_completo)

    # separar primeiro e último para email (apenas para formar algo)
    partes = nome_completo.split()
    primeiro_nome = partes[0]
    ultimo_sobrenome = partes[-1]

    # Cargo e salário
    cargo_escolhido = random.choice(list(cargos_ti.keys()))
    faixa = cargos_ti[cargo_escolhido]
    salario = random.randint(faixa[0], faixa[1])

    # IDADE REALISTA
    idade = gerar_idade_por_cargo(cargo_escolhido)

    # gerar email simples e garantir minúsculas e sem espaços
    email_local = f"{primeiro_nome.lower()}.{ultimo_sobrenome.lower()}"
    # se já existir muito igual, adicionar número randômico
    if sum(1 for f in funcionarios if f["email"].startswith(email_local)) > 5:
        email_local = f"{email_local}{random.randint(1,999)}"
    email = f"{email_local}@empresa.com.br"

    # telefone realista
    telefone = f"({random.randint(11, 99)}) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"

    funcionarios.append({
        "nome": nome_completo,
        "idade": idade,
        "email": email,
        "telefone": telefone,
        "cargo": cargo_escolhido,
        "salario": salario,
        "setor": "TI"
    })

# caso não tenha gerado 1000 por algum motivo, avisa
if len(funcionarios) < 1000:
    print(f"Atenção: foram gerados somente {len(funcionarios)} registros após {tentativas} tentativas.")
else:
    print(f"Gerados {len(funcionarios)} funcionários com sucesso em {tentativas} tentativas.")

# ------------------------------------------------------------
# 6. INSERÇÃO NO MONGODB (em lote)
# ------------------------------------------------------------
try:
    resultado = collection.insert_many(funcionarios)
    print(f"{len(resultado.inserted_ids)} registros inseridos com sucesso!")
except Exception as e:
    print("Erro ao inserir no MongoDB:", e)

