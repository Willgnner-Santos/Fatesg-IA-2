# Import das bibliotecas
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# Conexão com mongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Acessa o banco startup

db = client["startup"]

# aqui acessamos a coleção de funcionarios da empresa

collection = db['funcionarios']

# Aqui iniciaremos uma busca de dados no Mongo
# estamos procurando os dados (idade e salário)
data = list(
    collection.find({},
    {"_id": 0,
     "idade": 1,
     "salario": 1
     }                
                    )
)

# Converter para um DataFrame PANDAS
 
df = pd.DataFrame(data)

# Preparação dos dados para a regressão linear

X = df[["idade"]] # Variavel previsora

y = df['salario'] # Valor a ser previsto

# Divisão dos dados em conjunto de treino (80%) e teste (20%)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2)

# Criação do modelo

model= LinearRegression()

# Treinamento do modelo

model.fit(X_train, y_train)

# ===== INPUT DO USUÁRIO =====

print("="*50)
print("CALCULADORA DE SALÁRIO POR IDADE")
print("="*50)

try:
    idade_entrada = int(input("Digite a idade desejada: "))
    
    # Validar entrada
    if idade_entrada < 18 or idade_entrada > 65:
        print("Idade inválida! Use um valor entre 18 e 65.")
    else:
        # Fazer predição
        idade_nova = [[idade_entrada]]
        salario_predito = model.predict(idade_nova)
        
        print(f"\n Salário estimado para {idade_entrada} anos: R$ {salario_predito[0]:.2f}")
        
except ValueError:
    print("Erro! Digite um número válido.")

# ===== VISUALIZAÇÃO GRÁFICA =====

# Criar figura com dois gráficos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# --- Gráfico 1: Dados de treino com linha de regressão ---
ax1.scatter(X_train, y_train, color='blue', label='Dados de Treino', alpha=0.6)
ax1.scatter(X_test, y_test, color='red', label='Dados de Teste', alpha=0.6)

# Linha de regressão
X_linha = np.array([[X.min().values[0]], [X.max().values[0]]])
y_linha = model.predict(X_linha)
ax1.plot(X_linha, y_linha, color='green', linewidth=2, label='Linha de Regressão')

ax1.set_xlabel('Idade (anos)', fontsize=12)
ax1.set_ylabel('Salário (R$)', fontsize=12)
ax1.set_title('Regressão Linear: Idade vs Salário', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# --- Gráfico 2: Predição para idade = 30 ---
idades_futuras = np.array([[20], [30], [40], [50], [60]])
salarios_futuros = model.predict(idades_futuras)

ax2.plot(idades_futuras, salarios_futuros, 'g-', linewidth=2, label='Predição')
ax2.scatter(idades_futuras, salarios_futuros, color='orange', s=100, zorder=5)

# Adicionar ponto com a idade do usuário
try:
    ax2.scatter([idade_entrada], [salario_predito], color='red', s=200, marker='*', 
                label=f'Sua Predição ({idade_entrada} anos)', zorder=5)
except:
    pass

ax2.set_xlabel('Idade (anos)', fontsize=12)
ax2.set_ylabel('Salário Predito (R$)', fontsize=12)
ax2.set_title('Predições de Salário por Idade', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Exibir o gráfico
plt.tight_layout()
plt.show()

# Adicionar mais informações
print("\n" + "="*50)
print("ANÁLISE DO MODELO")
print("="*50)
print(f"Coeficiente (inclinação): {model.coef_[0]:.2f}")
print(f"Intercepto: {model.intercept_:.2f}")
print(f"Score (R²) - Treino: {model.score(X_train, y_train):.4f}")
print(f"Score (R²) - Teste: {model.score(X_test, y_test):.4f}")
print("="*50)