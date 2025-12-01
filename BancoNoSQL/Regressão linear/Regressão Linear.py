# Importação das bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from pymongo import MongoClient
import sys

print("=" * 60)
print("INICIANDO ANÁLISE DE REGRESSÃO LINEAR")
print("=" * 60)

# CONFIGURAÇÃO DA CONEXÃO - MODIFIQUE AQUI!
# Para MongoDB Atlas, use:
# MONGO_URI = "mongodb+srv://usuario:senha@cluster.mongodb.net/"
# Para MongoDB local, use:
MONGO_URI = "mongodb+srv://omoiomoi_db_user:c3tze90kRQYdoikb@regressaolinear.9mncybw.mongodb.net/?appName=Regressaolinear"

try:
    print("\n🔄 Tentando conectar ao MongoDB...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Testar a conexão
    client.admin.command('ping')
    print("✅ Conexão com MongoDB estabelecida com sucesso!")
    
except Exception as e:
    print(f"❌ ERRO ao conectar ao MongoDB: {e}")
    print("\n💡 SOLUÇÕES:")
    print("1. Se estiver usando MongoDB local, certifique-se de que está rodando")
    print("2. Se estiver usando Atlas, verifique:")
    print("   - A string de conexão está correta?")
    print("   - Substituiu <password> pela senha real?")
    print("   - Seu IP está liberado no Network Access?")
    sys.exit(1)

# Acessar banco e coleção
db = client["startup"]
collection = db["funcionarios"]

# Verificar se existem dados
try:
    count = collection.count_documents({})
    print(f"\n📊 Total de documentos na coleção 'funcionarios': {count}")
    
    if count == 0:
        print("\n⚠️  AVISO: Não há dados na coleção!")
        print("🔄 Inserindo dados de exemplo automaticamente...")
        
        # Dados de exemplo
        dados_exemplo = [
            {"idade": 25, "salario": 2800},
            {"idade": 30, "salario": 3500},
            {"idade": 35, "salario": 4200},
            {"idade": 28, "salario": 3200},
            {"idade": 42, "salario": 5500},
            {"idade": 38, "salario": 4800},
            {"idade": 45, "salario": 6000},
            {"idade": 32, "salario": 3900},
            {"idade": 50, "salario": 7200},
            {"idade": 29, "salario": 3400},
            {"idade": 55, "salario": 8000},
            {"idade": 40, "salario": 5200},
            {"idade": 33, "salario": 4100},
            {"idade": 48, "salario": 6500},
            {"idade": 27, "salario": 3000},
            {"idade": 36, "salario": 4500},
            {"idade": 44, "salario": 5800},
            {"idade": 31, "salario": 3700},
            {"idade": 52, "salario": 7500},
            {"idade": 26, "salario": 2900}
        ]
        
        collection.insert_many(dados_exemplo)
        count = collection.count_documents({})
        print(f"✅ {count} documentos inseridos com sucesso!")
    
except Exception as e:
    print(f"❌ ERRO ao acessar a coleção: {e}")
    sys.exit(1)

# Buscar os dados do MongoDB
try:
    data = list(collection.find({}, {"_id": 0, "idade": 1, "salario": 1}))
    print(f"✅ Dados recuperados com sucesso: {len(data)} registros")
except Exception as e:
    print(f"❌ ERRO ao buscar dados: {e}")
    sys.exit(1)

# Converter para DataFrame
df = pd.DataFrame(data)

# Verificar se o DataFrame não está vazio
if df.empty:
    print("\n❌ ERRO: O DataFrame está vazio!")
    print("💡 Verifique se os documentos no MongoDB têm os campos 'idade' e 'salario'")
    sys.exit(1)

# Verificar se as colunas esperadas existem
if 'idade' not in df.columns or 'salario' not in df.columns:
    print("\n❌ ERRO: Colunas 'idade' ou 'salario' não encontradas!")
    print(f"Colunas disponíveis: {df.columns.tolist()}")
    sys.exit(1)

print("\n" + "=" * 60)
print("1. ANÁLISE EXPLORATÓRIA DOS DADOS")
print("=" * 60)

# Verificar informações básicas
print("\n📋 Informações do Dataset:")
print(df.info())

# Verificar valores ausentes
print("\n\n🔍 Valores Ausentes:")
valores_ausentes = df.isnull().sum()
print(valores_ausentes)
if valores_ausentes.sum() == 0:
    print("✅ Nenhum valor ausente encontrado!")

# Verificar duplicatas
duplicatas = df.duplicated().sum()
print(f"\n🔍 Duplicatas encontradas: {duplicatas}")
if duplicatas == 0:
    print("✅ Nenhuma duplicata encontrada!")

# Estatísticas descritivas
print("\n\n📊 Estatísticas Descritivas:")
print(df.describe())

# Verificar valores inconsistentes
print("\n\n⚠️  Verificação de Valores Inconsistentes:")
idades_negativas = (df['idade'] < 0).sum()
salarios_negativos = (df['salario'] < 0).sum()
idades_altas = (df['idade'] > 100).sum()

print(f"Idades negativas: {idades_negativas}")
print(f"Salários negativos: {salarios_negativos}")
print(f"Idades muito altas (>100): {idades_altas}")

if idades_negativas == 0 and salarios_negativos == 0 and idades_altas == 0:
    print("✅ Nenhuma inconsistência encontrada!")

# Remover possíveis inconsistências
df_clean = df[(df['idade'] > 0) & (df['salario'] > 0) & (df['idade'] <= 100)].copy()
removidos = len(df) - len(df_clean)

if removidos > 0:
    print(f"\n🧹 Dados após limpeza: {len(df_clean)} registros ({removidos} removidos)")
else:
    print(f"\n✅ Todos os {len(df_clean)} registros estão limpos!")

# Verificar se ainda temos dados suficientes
if len(df_clean) < 5:
    print("\n❌ ERRO: Dados insuficientes para análise (mínimo 5 registros)")
    sys.exit(1)

print("\n" + "=" * 60)
print("2. ANÁLISE ESTATÍSTICA DETALHADA")
print("=" * 60)

print(f"\n👥 IDADE:")
print(f"   Média: {df_clean['idade'].mean():.2f} anos")
print(f"   Mediana: {df_clean['idade'].median():.2f} anos")
print(f"   Desvio Padrão: {df_clean['idade'].std():.2f} anos")
print(f"   Mínimo: {df_clean['idade'].min():.0f} anos")
print(f"   Máximo: {df_clean['idade'].max():.0f} anos")

print(f"\n💰 SALÁRIO:")
print(f"   Média: R$ {df_clean['salario'].mean():.2f}")
print(f"   Mediana: R$ {df_clean['salario'].median():.2f}")
print(f"   Desvio Padrão: R$ {df_clean['salario'].std():.2f}")
print(f"   Mínimo: R$ {df_clean['salario'].min():.2f}")
print(f"   Máximo: R$ {df_clean['salario'].max():.2f}")

# Correlação
correlacao = df_clean['idade'].corr(df_clean['salario'])
print(f"\n📈 Correlação entre Idade e Salário: {correlacao:.4f}")

# Dividir dados em treino e teste
X = df_clean[['idade']]
y = df_clean['salario']

# Ajustar test_size se tivermos poucos dados
if len(df_clean) < 10:
    test_size = 0.3
else:
    test_size = 0.2

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

print(f"\n📦 Divisão dos dados:")
print(f"   Treino: {len(X_train)} registros ({(1-test_size)*100:.0f}%)")
print(f"   Teste: {len(X_test)} registros ({test_size*100:.0f}%)")

# Treinar o modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)

print("\n" + "=" * 60)
print("3. AVALIAÇÃO DO MODELO")
print("=" * 60)

# Métricas do modelo
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"\n📐 Equação da Reta:")
print(f"   Salário = {model.intercept_:.2f} + {model.coef_[0]:.2f} × Idade")
print(f"\n   Coeficiente angular: {model.coef_[0]:.2f}")
print(f"   Intercepto: {model.intercept_:.2f}")

print(f"\n📊 Métricas de Avaliação:")
print(f"   MSE (Erro Quadrático Médio): {mse:.2f}")
print(f"   RMSE (Raiz do MSE): {rmse:.2f}")
print(f"   R² Score: {r2:.4f} ({r2*100:.2f}%)")

print("\n" + "=" * 60)
print("4. PREVISÕES PARA DIFERENTES IDADES")
print("=" * 60)

idades_teste = [25, 30, 35, 40, 45, 50, 55, 60]
print("\n💼 Previsões de Salário:")
print("-" * 40)
for idade in idades_teste:
    salario_previsto = model.predict([[idade]])[0]
    print(f"   {idade} anos → R$ {salario_previsto:,.2f}")

# GRÁFICOS
print("\n" + "=" * 60)
print("5. GERANDO VISUALIZAÇÕES")
print("=" * 60)

try:
    # Configurar estilo
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(16, 10))
    
    # Gráfico 1: Dispersão com linha de regressão
    plt.subplot(2, 3, 1)
    plt.scatter(X_train, y_train, color='blue', alpha=0.6, s=50, label='Treino', edgecolors='black', linewidth=0.5)
    plt.scatter(X_test, y_test, color='green', alpha=0.6, s=50, label='Teste', edgecolors='black', linewidth=0.5)
    plt.plot(X, model.predict(X), color='red', linewidth=2.5, label='Regressão Linear')
    plt.xlabel('Idade (anos)', fontsize=11, fontweight='bold')
    plt.ylabel('Salário (R$)', fontsize=11, fontweight='bold')
    plt.title('Regressão Linear: Idade vs Salário', fontsize=12, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfico 2: Valores Reais vs Preditos
    plt.subplot(2, 3, 2)
    plt.scatter(y_test, y_pred, color='purple', alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
             color='red', linewidth=2, linestyle='--', label='Predição Perfeita')
    plt.xlabel('Salário Real (R$)', fontsize=11, fontweight='bold')
    plt.ylabel('Salário Previsto (R$)', fontsize=11, fontweight='bold')
    plt.title('Valores Reais vs Preditos', fontsize=12, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfico 3: Resíduos
    plt.subplot(2, 3, 3)
    residuos = y_test - y_pred
    plt.scatter(y_pred, residuos, color='orange', alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
    plt.xlabel('Salário Previsto (R$)', fontsize=11, fontweight='bold')
    plt.ylabel('Resíduos', fontsize=11, fontweight='bold')
    plt.title('Análise de Resíduos', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Gráfico 4: Distribuição de Idades
    plt.subplot(2, 3, 4)
    plt.hist(df_clean['idade'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Idade (anos)', fontsize=11, fontweight='bold')
    plt.ylabel('Frequência', fontsize=11, fontweight='bold')
    plt.title('Distribuição de Idades', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Gráfico 5: Distribuição de Salários
    plt.subplot(2, 3, 5)
    plt.hist(df_clean['salario'], bins=15, color='lightgreen', edgecolor='black', alpha=0.7)
    plt.xlabel('Salário (R$)', fontsize=11, fontweight='bold')
    plt.ylabel('Frequência', fontsize=11, fontweight='bold')
    plt.title('Distribuição de Salários', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Gráfico 6: Boxplot comparativo
    plt.subplot(2, 3, 6)
    bp = plt.boxplot([df_clean['idade'], df_clean['salario']/1000], 
                      labels=['Idade (anos)', 'Salário (R$ mil)'],
                      patch_artist=True)
    for patch, color in zip(bp['boxes'], ['lightblue', 'lightcoral']):
        patch.set_facecolor(color)
    plt.title('Boxplot - Idade e Salário', fontsize=12, fontweight='bold')
    plt.ylabel('Valores', fontsize=11, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('analise_regressao_completa.png', dpi=300, bbox_inches='tight')
    print("\n✅ Gráficos salvos em 'analise_regressao_completa.png'")
    plt.show()
    
except Exception as e:
    print(f"\n⚠️  Aviso: Erro ao gerar gráficos: {e}")
    print("A análise foi concluída, mas os gráficos não puderam ser gerados.")

print("\n" + "=" * 60)
print("6. INSIGHTS E CONCLUSÕES")
print("=" * 60)

print("\n🔍 Interpretação dos Resultados:")

# Análise da correlação
print(f"\n📊 Correlação ({correlacao:.4f}):")
if abs(correlacao) > 0.7:
    intensidade = "FORTE"
    emoji = "💪"
elif abs(correlacao) > 0.4:
    intensidade = "MODERADA"
    emoji = "👍"
else:
    intensidade = "FRACA"
    emoji = "⚠️"

print(f"   {emoji} Relação {intensidade} entre idade e salário")

# Análise do R²
print(f"\n📈 R² Score ({r2:.4f}):")
print(f"   O modelo explica {r2*100:.2f}% da variação nos salários")

if r2 > 0.7:
    print("   ✅ Excelente poder explicativo!")
elif r2 > 0.5:
    print("   👍 Bom poder explicativo")
elif r2 > 0.3:
    print("   ⚠️  Poder explicativo moderado")
else:
    print("   ❌ Baixo poder explicativo")

# Interpretação do coeficiente
print(f"\n💰 Impacto da Idade no Salário:")
print(f"   Para cada ano adicional, o salário aumenta R$ {model.coef_[0]:.2f}")

if r2 < 0.5:
    print("\n⚠️  ATENÇÃO: O modelo tem limitações")
    print("   Possíveis causas:")
    print("   • Poucos dados disponíveis")
    print("   • Alta dispersão nos valores de salário")
    print("   • Outras variáveis importantes não consideradas:")
    print("     - Cargo/Posição")
    print("     - Tempo de experiência")
    print("     - Nível educacional")
    print("     - Setor de atuação")

print("\n" + "=" * 60)
print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
print("=" * 60)
print("\n📁 Arquivos gerados:")
print("   • analise_regressao_completa.png (gráficos)")
print("\n💡 Dica: Use este terminal e a imagem para sua entrega!")
print("=" * 60)