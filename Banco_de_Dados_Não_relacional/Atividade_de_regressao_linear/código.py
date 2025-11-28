import pymongo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#Configuração de estilo para os gráficos
sns.set_theme(style="whitegrid")

#  ---------------------------------------------------------
# Fatesg - Banco de Dados noSQL - Análise de Salários
# Aluno: Letícia Alves Peixoto de Barros
# ---------------------------------------------------------

# ---------------------------------------------------------
# 1. CONEXÃO COM O MONGODB
# ---------------------------------------------------------
print("--- Conectando ao MongoDB ---")
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["startup"]
    collection = db["funcionarios"]
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar no MongoDB: {e}")
    exit()

# ---------------------------------------------------------
# 2. VERIFICAÇÃO E INSERÇÃO DE DADOS (MOCK DATA)
# ---------------------------------------------------------
# Se não houver dados, vamos inserir alguns para a atividade funcionar
if collection.count_documents({}) == 0:
    print("Coleção vazia. Inserindo dados fictícios para teste...")
    dados_ficticios = [
        {"idade": 20, "salario": 1500}, {"idade": 21, "salario": 1600},
        {"idade": 25, "salario": 2800}, {"idade": 24, "salario": 2600},
        {"idade": 30, "salario": 4000}, {"idade": 32, "salario": 4200},
        {"idade": 40, "salario": 6500}, {"idade": 45, "salario": 7000},
        {"idade": 50, "salario": 8500}, {"idade": 19, "salario": 1400},
        {"idade": 55, "salario": 9200}, {"idade": 60, "salario": 10500},
        {"idade": None, "salario": 5000},
        {"idade": 28, "salario": -100}    
    ]
    collection.insert_many(dados_ficticios)
    print(f"{len(dados_ficticios)} documentos inseridos.")

# ---------------------------------------------------------
# 3. CARREGAMENTO E LIMPEZA DOS DADOS
# ---------------------------------------------------------
print("\n--- Carregando Dados ---")
data = list(collection.find({}, {"_id": 0, "idade": 1, "salario": 1}))
df = pd.DataFrame(data)

print(f"Total de registros originais: {len(df)}")

# Análise de Valores Ausentes
print("\nVerificando valores nulos:")
print(df.isnull().sum())

# Limpeza: Remover linhas com NaN e valores inconsistentes (salário negativo ou idade zero/negativa)
df_clean = df.dropna()
df_clean = df_clean[(df_clean['salario'] > 0) & (df_clean['idade'] > 0)]

print(f"\nRegistros após limpeza: {len(df_clean)}")
print("\nEstatísticas Descritivas:")
print(df_clean.describe())

# ---------------------------------------------------------
# 4. MODELAGEM (REGRESSÃO LINEAR)
# ---------------------------------------------------------
X = df_clean[["idade"]]
y = df_clean["salario"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# ---------------------------------------------------------
# 5. PREVISÕES E AVALIAÇÃO
# ---------------------------------------------------------
print("\n--- Previsões Solicitadas ---")
idades_para_prever = np.array([[30], [40], [50]])
salarios_preditos = model.predict(idades_para_prever)

for idade, salario in zip(idades_para_prever, salarios_preditos):
    print(f"Idade: {idade[0]} anos -> Salário estimado: R$ {salario:.2f}")

# Avaliação do Modelo
y_pred_test = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred_test)
r2 = r2_score(y_test, y_pred_test)

print("\n--- Avaliação do Modelo ---")
print(f"Erro Quadrático Médio (MSE): {mse:.2f}")
print(f"R² Score (Coeficiente de Determinação): {r2:.4f}")
print("OBS: Um R² próximo de 1.0 indica que o modelo explica bem os dados.")

# ---------------------------------------------------------
# 6. GERAÇÃO DE GRÁFICOS
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# Plotar os pontos reais (Dispersão)
plt.scatter(df_clean['idade'], df_clean['salario'], color='blue', label='Dados Reais')

# Plotar a linha de regressão (Tendência)
# Criar linha: menor idade até a maior idade do dataset
linha_X = np.linspace(df_clean['idade'].min(), df_clean['idade'].max(), 100).reshape(-1, 1)
linha_y = model.predict(linha_X)
plt.plot(linha_X, linha_y, color='red', linewidth=2, label='Linha de Tendência (Regressão)')

plt.title('Regressão Linear: Idade vs Salário')
plt.xlabel('Idade (Anos)')
plt.ylabel('Salário (R$)')
plt.legend()
plt.grid(True, alpha=0.3)

# Salvar o gráfico 
plt.savefig("grafico_regressao.png")
print("\nGráfico gerado e salvo como 'grafico_regressao.png'. Exibindo na tela...")
plt.show()
