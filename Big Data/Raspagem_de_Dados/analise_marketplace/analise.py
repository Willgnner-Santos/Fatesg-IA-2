# Importa as bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1) CARREGAMENTO E INSPEÇÃO DOS DADOS DO MARKETPLACE

# Substitua pelo caminho correto do seu arquivo JSON
file_path = r'C:\Users\aluno\Desktop\wiuwiuwiu\dataset_facebook-groups-scraper_2025-11-10_23-07-12-863 (1).json'
if os.path.exists(file_path):
    df = pd.read_json(file_path)
    print(f"Dados carregados: {df.shape[0]} linhas e {df.shape[1]} colunas.")
else:
    print(f"ERRO: Arquivo '{file_path}' não encontrado. Por favor, insira seus dados.")
    exit()

print("\n--- Primeiras linhas dos dados ---")
print(df.head())
print("\n--- Tipos de dados (Dtypes) ---")
print(df.info())

# 2) ESTATÍSTICAS DESCRITIVAS EM COLUNAS NUMÉRICAS
# Colunas numéricas típicas: 'Preco', 'Custo', 'Lucro', 'TempoDeEspera (dias)'
print("\n=== ESTATÍSTICAS NUMÉRICAS (Preço/Lucro) ===")
# Adapte as colunas conforme o seu dataset
numeric_cols = ['Preco', 'Lucro'] 
print(df[numeric_cols].describe())

# 3) ANÁLISE DE VENDAS POR CATEGORIA E STATUS
# Contagem de valores (frequência) em colunas categóricas
print("\n=== FREQUÊNCIA DE CATEGORIAS ===")
# Exemplo: 'Categoria' (Roupas, Eletrônicos, Móveis)
print(df['Categoria'].value_counts())

print("\n=== FREQUÊNCIA DO STATUS DA VENDA ===")
# Exemplo: 'Status' (Vendido, Em Negociação, Expirado)
print(df['Status'].value_counts())

# 4) VISUALIZAÇÕES DE VENDAS (Exemplos)

# Histograma da Distribuição de Preços
plt.figure(figsize=(10, 6))
sns.histplot(df['Preco'], bins=20, kde=True)
plt.title('Distribuição de Preços dos Itens no Marketplace')
plt.xlabel('Preço (R$)')
plt.ylabel('Frequência')
plt.show()

# Boxplot para Outliers de Lucro por Categoria (Adapte 'Lucro' e 'Categoria')
plt.figure(figsize=(12, 7))
sns.boxplot(x='Categoria', y='Lucro', data=df) 
plt.title('Boxplot do Lucro por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Lucro (R$)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Scatterplot (Se você tiver a coluna de 'Avaliacao_Comprador' vs 'Preco')
# Se não tiver dados de avaliação, use duas colunas numéricas de interesse (ex: 'Lucro' vs 'Preco')
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='Preco', y='Lucro', data=df)
# plt.title('Relação entre Preço e Lucro')
# plt.show()