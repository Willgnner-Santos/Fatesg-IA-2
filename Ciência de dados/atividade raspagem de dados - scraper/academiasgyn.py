import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações iniciais
FILEPATH = r"C:\Users\rafae\OneDrive\Documentos\dataset_crawler-google-places_2025-11-10_23-10-33-209.json"
TOP_N_CATEGORIES = 10
sns.set_theme(style="whitegrid")

# Checar existência do arquivo
if not os.path.exists(FILEPATH):
    raise FileNotFoundError(f"Arquivo não encontrado em {FILEPATH}, ajuste o caminho.")

# Carregar dados
df = pd.read_json(FILEPATH, orient='records')

# Exibir informações básicas
print("Shape do dataset:", df.shape)
print(df.dtypes)
print(df.head())

# Estatísticas descritivas das colunas numéricas principais
print(df[['totalScore', 'reviewsCount']].describe())

# Contagem das principais categorias
if 'categoryName' in df.columns:
    cat_counts = df['categoryName'].value_counts().head(TOP_N_CATEGORIES)
    print(f"Top {TOP_N_CATEGORIES} categorias:")
    print(cat_counts)

# Contagem das cidades
if 'city' in df.columns:
    city_counts = df['city'].value_counts()
    print("Contagem por cidade:")
    print(city_counts)

# Plot barras das principais categorias
plt.figure(figsize=(8, 5))
sns.barplot(x=cat_counts.values, y=cat_counts.index)
plt.title(f"Top {TOP_N_CATEGORIES} Categorias de Academias")
plt.xlabel("Frequência")
plt.ylabel("Categoria")
plt.tight_layout()
plt.show()

# Histogramas de totalScore e reviewsCount
plt.figure(figsize=(6, 4))
sns.histplot(df['totalScore'].dropna(), bins=10, kde=False)
plt.title("Distribuição de Total Score")
plt.xlabel("Nota Média")
plt.ylabel("Frequência")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 4))
sns.histplot(df['reviewsCount'].dropna(), bins=10, kde=False)
plt.title("Distribuição de Número de Avaliações")
plt.xlabel("Número de Avaliações")
plt.ylabel("Frequência")
plt.tight_layout()
plt.show()

# Boxplots para verificar outliers
plt.figure(figsize=(5, 6))
sns.boxplot(y=df['totalScore'].dropna())
plt.title("Boxplot de Total Score")
plt.ylabel("Nota Média")
plt.tight_layout()
plt.show()

plt.figure(figsize=(5, 6))
sns.boxplot(y=df['reviewsCount'].dropna())
plt.title("Boxplot de Número de Avaliações")
plt.ylabel("Número de Avaliações")
plt.tight_layout()
plt.show()

# Scatter plot de reviewsCount vs totalScore
plt.figure(figsize=(6, 4))
sns.scatterplot(x=df['reviewsCount'], y=df['totalScore'], alpha=0.7)
plt.title("Dispersão: Número de Avaliações x Nota Média")
plt.xlabel("Número de Avaliações")
plt.ylabel("Nota Média")
plt.tight_layout()
plt.show()
