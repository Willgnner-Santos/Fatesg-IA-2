import pymongo
import pandas as pd
import random
import numpy as np
from faker import Faker

# ============== CONEXÃO COM MONGODB ==============
try:
    client = pymongo.MongoClient("mongodb+srv://PedroVaz-2:pedrovaz123A@chatbot.2y9ppso.mongodb.net/?appName=Chatbot")
    db = client["startup"]
    print("✓ Conexão com MongoDB estabelecida")
except Exception as e:
    print(f"✗ Erro ao conectar: {e}")
    exit()

# ============== VERIFICAR BANCO E COLEÇÕES ==============
print(f"\nBancos de dados disponíveis: {client.list_database_names()}")
print(f"Coleções no banco 'startup': {db.list_collection_names()}")

# ============== VERIFICAR DADOS EXISTENTES ==============
collection = db["funcionarios"]
count = collection.count_documents({})
print(f"\nDocumentos na coleção 'funcionarios': {count}")

if count > 0:
    resposta = input("\n⚠ A coleção já tem dados. Deseja sobrescrever? (s/n): ").strip().lower()
    if resposta == 's':
        collection.delete_many({})
        print("✓ Dados anteriores removidos")
    else:
        print("Operação cancelada.")
        exit()

# ============== INICIALIZAR FAKER ==============
fake = Faker('pt_BR')

# ============== DEFINIR POSIÇÕES E RANGES DE SALÁRIO ==============
posicoes = {
    "Estagiário": {"salario_min": 1800, "salario_max": 2500, "repeticoes": 12},
    "Assistente de Desenvolvimento": {"salario_min": 2200, "salario_max": 3200, "repeticoes": 10},
    "Desenvolvedor Júnior": {"salario_min": 2800, "salario_max": 4000, "repeticoes": 15},
    "Desenvolvedor Pleno": {"salario_min": 4000, "salario_max": 6500, "repeticoes": 18},
    "Desenvolvedor Sênior": {"salario_min": 6000, "salario_max": 8500, "repeticoes": 12},
    "Arquiteto de Jogos": {"salario_min": 7000, "salario_max": 10000, "repeticoes": 8},
    "Designer Gráfico": {"salario_min": 2500, "salario_max": 4500, "repeticoes": 10},
    "Designer de Níveis": {"salario_min": 3000, "salario_max": 5500, "repeticoes": 8},
    "Gerente de Projeto": {"salario_min": 5000, "salario_max": 8000, "repeticoes": 7},
    "Líder de Equipe": {"salario_min": 6000, "salario_max": 9000, "repeticoes": 6},
    "QA Tester": {"salario_min": 2000, "salario_max": 3500, "repeticoes": 12},
    "QA Automação": {"salario_min": 3000, "salario_max": 5000, "repeticoes": 10},
    "Animador": {"salario_min": 2800, "salario_max": 4800, "repeticoes": 9},
    "Sound Designer": {"salario_min": 2500, "salario_max": 4500, "repeticoes": 7},
    "Producer": {"salario_min": 4500, "salario_max": 7500, "repeticoes": 8},
    "Community Manager": {"salario_min": 2000, "salario_max": 3500, "repeticoes": 6},
    "DevOps": {"salario_min": 5500, "salario_max": 8500, "repeticoes": 5},
    "Business Analyst": {"salario_min": 3500, "salario_max": 5500, "repeticoes": 6},
}

# ============== GERAR DADOS RANDOMIZADOS ==============
print("\n🎮 Gerando dados randomizados para empresa de jogos...\n")

np.random.seed(42)
random.seed(42)
Faker.seed(42)

dados_teste = []
nomes_usados = set()

# Para cada posição, gerar múltiplos funcionários
for posicao, config in posicoes.items():
    repeticoes = config["repeticoes"]
    
    for rep in range(repeticoes):
        # Gerar nome único
        nome = fake.name()
        while nome in nomes_usados:
            nome = fake.name()
        nomes_usados.add(nome)
        
        # Gerar idade com distribuição realista
        # Posições mais sênior tendem a ter pessoas mais velhas
        if "Sênior" in posicao or "Arquiteto" in posicao or "Líder" in posicao or "Gerente" in posicao or "Producer" in posicao:
            idade = np.random.normal(loc=45, scale=10)
        elif "Júnior" in posicao or "Assistente" in posicao or "Estagiário" in posicao:
            idade = np.random.normal(loc=26, scale=5)
        else:
            idade = np.random.normal(loc=35, scale=10)
        
        idade = int(np.clip(idade, 20, 65))
        
        # Gerar salário baseado na posição com variação
        salario_min = config["salario_min"]
        salario_max = config["salario_max"]
        
        # Variação extra baseada na idade (mais experiência = melhor salário)
        idade_normalizada = (idade - 20) / 45
        variacao_idade = idade_normalizada * 0.25  # 25% de variação baseada na idade
        
        # Variação por performance/experiência na posição
        variacao_performance = random.uniform(-0.15, 0.20)  # ±15% a +20%
        
        salario_base = random.uniform(salario_min, salario_max)
        salario = salario_base * (1 + variacao_idade + variacao_performance)
        
        # Adicionar pequeno bônus/descontos aleatórios
        variacao_bonus = random.uniform(-100, 300)
        salario = round(salario + variacao_bonus, 2)
        
        # Garantir que o salário está dentro de um range razoável
        salario = max(salario, salario_min * 0.85)
        salario = min(salario, salario_max * 1.15)
        salario = round(salario, 2)
        
        # Gerar email profissional
        email = f"{nome.lower().replace(' ', '.')}@gamesstudio.com"
        
        # Gerar departamento baseado na posição
        if "Desenvolvedor" in posicao or "Arquiteto" in posicao or "DevOps" in posicao:
            departamento = "Desenvolvimento"
        elif "Designer" in posicao or "Animador" in posicao:
            departamento = "Design"
        elif "QA" in posicao:
            departamento = "Qualidade"
        elif "Gerente" in posicao or "Líder" in posicao or "Producer" in posicao:
            departamento = "Gestão"
        elif "Community" in posicao:
            departamento = "Marketing"
        else:
            departamento = "Suporte"
        
        # Gerar tempo de empresa (em meses)
        tempo_empresa = random.randint(3, 120)
        
        dados_teste.append({
            "nome": nome,
            "idade": idade,
            "salario": salario,
            "posicao": posicao,
            "departamento": departamento,
            "email": email,
            "tempo_empresa_meses": tempo_empresa
        })

# ============== INSERIR DADOS NO MONGODB ==============
try:
    result = collection.insert_many(dados_teste)
    print(f"✓ {len(result.inserted_ids)} documentos inseridos com sucesso!\n")
    
    # ============== EXIBIR ESTATÍSTICAS ==============
    print("="*80)
    print("ESTATÍSTICAS DOS DADOS INSERIDOS")
    print("="*80)
    
    df = pd.DataFrame(dados_teste)
    
    print(f"\n📊 Resumo Geral:")
    print(f"   Total de funcionários: {len(df)}")
    print(f"   Idade média: {df['idade'].mean():.1f} anos")
    print(f"   Idade mín/máx: {df['idade'].min()}/{df['idade'].max()} anos")
    print(f"   Salário médio: R$ {df['salario'].mean():.2f}")
    print(f"   Salário mín/máx: R$ {df['salario'].min():.2f} / R$ {df['salario'].max():.2f}")
    
    print(f"\n👥 Distribuição por Posição:")
    posicoes_count = df['posicao'].value_counts().sort_values(ascending=False)
    for pos, count in posicoes_count.items():
        salario_medio = df[df['posicao'] == pos]['salario'].mean()
        idade_media = df[df['posicao'] == pos]['idade'].mean()
        print(f"   {pos:.<38} {count:>3} | Idade: {idade_media:>5.1f} | Salário: R$ {salario_medio:.2f}")
    
    print(f"\n🏢 Distribuição por Departamento:")
    depts = df['departamento'].value_counts()
    for dept, count in depts.items():
        print(f"   {dept:.<38} {count:>3} funcionários")
    
    print(f"\n💰 Salários por Posição (Min - Máx - Média):")
    for pos in sorted(posicoes_list := list(posicoes.keys())):
        dados_pos = df[df['posicao'] == pos]
        if len(dados_pos) > 0:
            print(f"   {pos:.<38} R$ {dados_pos['salario'].min():>8.2f} - R$ {dados_pos['salario'].max():>8.2f} (Média: R$ {dados_pos['salario'].mean():>8.2f})")
    
    print(f"\n👤 Amostra de 5 funcionários:")
    amostra = df.sample(min(5, len(df)))[['nome', 'idade', 'posicao', 'salario', 'departamento']]
    for idx, row in amostra.iterrows():
        print(f"   {row['nome']:.<30} {row['idade']:>3} anos | {row['posicao']:.<25} | R$ {row['salario']:>8.2f} | {row['departamento']}")
    
    print("\n" + "="*80)
    print("PRÓXIMOS PASSOS:")
    print("="*80)
    print("Execute: python AnálisedeSalários.py")
    print("="*80)

except Exception as e:
    print(f"✗ Erro ao inserir dados: {e}")