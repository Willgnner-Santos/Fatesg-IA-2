import pymongo
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

# ============== CONEXÃO COM MONGODB ==============
try:
    client = pymongo.MongoClient("mongodb+srv://felipefatesg_db_user:1234@chatbot.mrcuhu0.mongodb.net/?appName=Chatbot")
    db = client["startup"]
    collection = db["funcionarios"]
    print("✓ Conexão com MongoDB estabelecida")
except Exception as e:
    print(f"✗ Erro ao conectar: {e}")
    exit()

# ============== BUSCAR E EXPLORAR DADOS ==============
try:
    data = list(collection.find({}, {"_id": 0}))
    print(f"\n✓ {len(data)} registros encontrados no banco de dados")
    
    if len(data) == 0:
        print("✗ Nenhum dado encontrado!")
        exit()
    
    df = pd.DataFrame(data)
    print(f"\nColunas disponíveis: {df.columns.tolist()}")
    print(f"Dimensões do DataFrame: {df.shape}")
    
except Exception as e:
    print(f"✗ Erro ao buscar dados: {e}")
    exit()

# ============== ANÁLISE DE DADOS ==============
print("\n--- ANÁLISE DOS DADOS ---")
print(df.head())
print(f"\nTipos de dados:\n{df.dtypes}")
print(f"\nValores ausentes:\n{df.isnull().sum()}")
print(f"\nEstatísticas descritivas:\n{df.describe()}")

# ============== LIMPEZA E PREPARAÇÃO DOS DADOS ==============
df_clean = df[['idade', 'salario', 'posicao', 'departamento', 'tempo_empresa_meses']].copy()

# Remover valores nulos
print(f"\nValores ausentes antes da limpeza: {df_clean.isnull().sum().sum()}")
df_clean = df_clean.dropna()
print(f"Valores ausentes após limpeza: {df_clean.isnull().sum().sum()}")

# Remover duplicatas
print(f"Linhas antes de remover duplicatas: {len(df_clean)}")
df_clean = df_clean.drop_duplicates(subset=['idade', 'salario', 'posicao'], keep='first')
print(f"Linhas após remover duplicatas: {len(df_clean)}")

# Verificar valores inconsistentes
print(f"\nIdade mínima: {df_clean['idade'].min()}, Máxima: {df_clean['idade'].max()}")
print(f"Salário mínimo: R$ {df_clean['salario'].min():.2f}, Máximo: R$ {df_clean['salario'].max():.2f}")

# Remover outliers extremos
df_clean = df_clean[(df_clean['idade'] > 0) & (df_clean['salario'] > 0)]
print(f"Registros após validação: {len(df_clean)}")

# ============== PREPARAÇÃO PARA O MODELO ==============
X = df_clean[["idade"]]
y = df_clean["salario"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nDados de treino: {len(X_train)}")
print(f"Dados de teste: {len(X_test)}")

# ============== TREINAMENTO DO MODELO ==============
model = LinearRegression()
model.fit(X_train, y_train)

print(f"\nCoeficiente (inclinação): {model.coef_[0]:.4f}")
print(f"Intercepto: {model.intercept_:.4f}")
print(f"Equação: Salário = {model.intercept_:.2f} + {model.coef_[0]:.2f} × Idade")

# ============== AVALIAÇÃO DO MODELO ==============
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
mae_test = mean_absolute_error(y_test, y_pred_test)

print(f"\n--- MÉTRICAS DO MODELO ---")
print(f"R² (Treino): {r2_train:.4f}")
print(f"R² (Teste): {r2_test:.4f}")
print(f"RMSE (Teste): R$ {rmse_test:.2f}")
print(f"MAE (Teste): R$ {mae_test:.2f}")

if r2_test < 0.3:
    print("\n⚠ Alerta: O modelo tem baixa precisão (R² < 0.3)")
    print("Possíveis causas: muita dispersão de dados, relação não-linear, ou variações de posição")

# ============== PREVISÕES ==============
idades_pred = [25, 30, 35, 40, 45, 50, 55, 60]
print(f"\n--- PREVISÕES DE SALÁRIOS PELA IDADE ---")
for idade in idades_pred:
    salario = model.predict([[idade]])[0]
    print(f"Idade {idade:>2} anos: R$ {salario:>8.2f}")

# ============== ANÁLISE POR POSIÇÃO ==============
print(f"\n--- ANÁLISE POR POSIÇÃO ---")
posicoes_stats = df_clean.groupby('posicao').agg({
    'salario': ['count', 'min', 'max', 'mean', 'std'],
    'idade': 'mean',
    'tempo_empresa_meses': 'mean'
}).round(2)

print(posicoes_stats)

# ============== ANÁLISE POR DEPARTAMENTO ==============
print(f"\n--- ANÁLISE POR DEPARTAMENTO ---")
dept_stats = df_clean.groupby('departamento').agg({
    'salario': ['count', 'min', 'max', 'mean'],
    'idade': 'mean'
}).round(2)

print(dept_stats)

# ============== VISUALIZAÇÕES ==============
plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Gráfico 1: Dispersão com linha de tendência
ax1 = fig.add_subplot(gs[0, :2])
ax1.scatter(X_train, y_train, alpha=0.6, label='Dados de treino', color='blue', s=50)
ax1.scatter(X_test, y_test, alpha=0.6, label='Dados de teste', color='red', s=50)
x_range = np.array([[X['idade'].min()], [X['idade'].max()]])
y_line = model.predict(x_range)
ax1.plot(x_range, y_line, 'g-', linewidth=2.5, label='Linha de tendência')
ax1.set_xlabel('Idade (anos)', fontsize=11)
ax1.set_ylabel('Salário (R$)', fontsize=11)
ax1.set_title('Regressão Linear: Idade vs Salário', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Gráfico 2: Métricas do modelo
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
metricas_texto = f"""
MÉTRICAS DO MODELO

R² (Treino): {r2_train:.4f}
R² (Teste): {r2_test:.4f}
RMSE: R$ {rmse_test:.2f}
MAE: R$ {mae_test:.2f}

EQUAÇÃO:
Salário = {model.intercept_:.2f}
         + {model.coef_[0]:.2f} × Idade

DADOS:
Total: {len(df_clean)}
Treino: {len(X_train)}
Teste: {len(X_test)}
"""
ax2.text(0.1, 0.5, metricas_texto, fontsize=10, verticalalignment='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), family='monospace')

# Gráfico 3: Resíduos
ax3 = fig.add_subplot(gs[1, 0])
residuos = y_test - y_pred_test
ax3.scatter(y_pred_test, residuos, alpha=0.6, color='purple', s=50)
ax3.axhline(y=0, color='r', linestyle='--', linewidth=2)
ax3.set_xlabel('Valores Preditos (R$)', fontsize=11)
ax3.set_ylabel('Resíduos (R$)', fontsize=11)
ax3.set_title('Análise de Resíduos', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)

# Gráfico 4: Distribuição dos resíduos
ax4 = fig.add_subplot(gs[1, 1])
ax4.hist(residuos, bins=20, edgecolor='black', alpha=0.7, color='orange')
ax4.set_xlabel('Resíduos (R$)', fontsize=11)
ax4.set_ylabel('Frequência', fontsize=11)
ax4.set_title('Distribuição dos Resíduos', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

# Gráfico 5: Valores reais vs preditos
ax5 = fig.add_subplot(gs[1, 2])
ax5.scatter(y_test, y_pred_test, alpha=0.6, color='green', s=50)
ax5.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
ax5.set_xlabel('Salário Real (R$)', fontsize=11)
ax5.set_ylabel('Salário Predito (R$)', fontsize=11)
ax5.set_title('Valores Reais vs Preditos', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3)

# Gráfico 6: Salário por Posição (Box plot)
ax6 = fig.add_subplot(gs[2, :2])
posicoes_ordem = df_clean.groupby('posicao')['salario'].median().sort_values(ascending=False).index
df_clean_sorted = df_clean.copy()
df_clean_sorted['posicao'] = pd.Categorical(df_clean_sorted['posicao'], categories=posicoes_ordem, ordered=True)
sns.boxplot(data=df_clean_sorted, x='posicao', y='salario', ax=ax6, palette='Set2')
ax6.set_xlabel('Posição', fontsize=11)
ax6.set_ylabel('Salário (R$)', fontsize=11)
ax6.set_title('Distribuição de Salários por Posição', fontsize=12, fontweight='bold')
ax6.tick_params(axis='x', rotation=45)
plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Gráfico 7: Salário por Departamento (Bar plot)
ax7 = fig.add_subplot(gs[2, 2])
dept_media = df_clean.groupby('departamento')['salario'].mean().sort_values(ascending=True)
dept_media.plot(kind='barh', ax=ax7, color='skyblue', edgecolor='black')
ax7.set_xlabel('Salário Médio (R$)', fontsize=11)
ax7.set_ylabel('Departamento', fontsize=11)
ax7.set_title('Salário Médio por Departamento', fontsize=12, fontweight='bold')
ax7.grid(True, alpha=0.3, axis='x')

plt.suptitle('Análise Completa de Salários - Empresa de Jogos', fontsize=14, fontweight='bold', y=0.995)
plt.savefig('analise_salarios_completa.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráficos salvos em 'analise_salarios_completa.png'")
plt.show()

print("\n" + "="*80)
print("ANÁLISE CONCLUÍDA COM SUCESSO")
print("="*80)