# Importação das bibliotecas necessárias
import pymongo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Configuração de estilo para os gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [10, 6]

print("--- Análise de Regressão Linear: Idade vs. Salário ---")

# 1. CONEXÃO COM O MONGODB E BUSCA DE DADOS
# =========================================
try:
    # Acessando o DB e a coleção criados pelo gerador de dados
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["TT_Ifood"]  # Nome do DB usado no gerador
    collection = db["funcionarios"]  # Nome da coleção usado no gerador

    # Buscar os dados necessários: idade e salario
    data = list(collection.find({}, {"_id": 0, "idade": 1, "salario": 1}))
    df = pd.DataFrame(data)

    if df.empty:
        print("\nERRO: DataFrame vazio. Certifique-se de que o MongoDB está rodando e o script gerador foi executado.")
        exit()
    print(f"\nDados carregados com sucesso. Total de {len(df)} registros.")

except Exception as e:
    print(f"\nERRO de Conexão ou Carga de Dados do MongoDB: {e}")
    exit()

# 2. MELHORAR A ANÁLISE DOS DADOS (Verificação e Estatísticas Descritivas)
# =======================================================================

print("\n--- 2. Análise de Consistência dos Dados ---")
# Checar por valores ausentes
print("Valores ausentes por coluna:\n", df.isnull().sum())

# Estatísticas descritivas do Salário
print("\nEstatísticas Descritivas do Salário (R$):\n", 
      df['salario'].describe().apply(lambda x: f'{x:,.2f}').to_string())

# Verificação simples de inconsistência (se houver salários zero ou idades fora do limite)
# O gerador garante dados consistentes, mas esta é a checagem que seria feita:
if (df['salario'] <= 0).any() or (df['idade'] < 18).any():
    print("\nAVISO: Inconsistências (salário <= 0 ou idade < 18) detectadas e removidas para a modelagem.")
    df = df[(df['salario'] > 0) & (df['idade'] >= 18)]


# 3. PREPARAÇÃO E TREINAMENTO DO MODELO
# ====================================
X = df[['idade']]  # Variável Independente (Idade)
y = df['salario']  # Variável Dependente (Salário)

# Dividir os dados em treino (80%) e teste (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo de regressão linear
model = LinearRegression()
model.fit(X_train, y_train) 
print("\nModelo de Regressão Linear treinado com 80% dos dados.")


# 4. ANÁLISE DE POSSÍVEIS ERROS (Métricas)
# =======================================
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
coeficiente = model.coef_[0]
intercepto = model.intercept_

print("\n--- 4. Análise de Erros e Métricas do Modelo ---")
print(f"R-squared (R²): {r2:.4f} (Qualidade do ajuste: próximo de 1 é melhor)")
print(f"Erro Quadrático Médio (MSE): {mse:,.2f}")
print(f"Coeficiente Angular (Declive): R$ {coeficiente:,.2f}")
print(f"Intercepto (Salário Base): R$ {intercepto:,.2f}")

# Explicação do R²:
if r2 < 0.5:
    print("\nInsight (Regressão): O R² baixo indica que 'Idade' sozinha não é uma forte preditora de 'Salário'. A dispersão dos dados é alta (como esperado em RH), sendo influenciada por outras variáveis (Cargo, Setor, Nível, etc.), conforme evidenciado no gráfico de dispersão.")
else:
    print("\nInsight (Regressão): O R² é razoável, indicando que a idade tem uma influência moderada no salário.")

# 5. GERAR GRÁFICOS (Visualização)
# ===============================

print("\n--- 5. Geração de Gráficos ---")

# Gráfico de Dispersão (Scatter Plot) com a Linha de Regressão
plt.figure(figsize=(10, 6))
# Plotar os pontos de dados
sns.scatterplot(x='idade', y='salario', data=df, color='skyblue', alpha=0.6, label='Dados Reais')
# Plotar a linha de regressão
plt.plot(X_test, y_pred, color='red', linewidth=2, label=f'Regressão Linear (R²: {r2:.2f})')
plt.title('Regressão Linear: Relação entre Idade e Salário')
plt.xlabel('Idade')
plt.ylabel('Salário (R$)')
plt.legend()
plt.show()

print("Gráfico de dispersão gerado. (A linha vermelha é o modelo de predição)")


# 6. FAZER PREVISÕES (Novas Idades)
# =================================
prever_idades = np.array([30, 40, 50, 60]).reshape(-1, 1)

# Usamos o modelo treinado para prever os salários
salarios_preditos = model.predict(prever_idades)

print("\n--- 6. Previsões de Salário para Diferentes Idades ---")
for idade, salario in zip(prever_idades.flatten(), salarios_preditos):
    print(f"Salário estimado para {idade} anos: R$ {salario:,.2f}")

print("\n--- FIM DA ANÁLISE ---")
