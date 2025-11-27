import pandas as pd
import numpy as np

# 1) Abrir o dataset CSV
print("=" * 80)
print("ANÁLISE EXPLORATÓRIA DO DATASET TITANIC")
print("=" * 80)

# Carregando o arquivo CSV
df = pd.read_csv('titanic.csv')

# 2) Exibir as 8 primeiras linhas
print("\n1. PRIMEIRAS 8 LINHAS DO DATASET:")
print("-" * 80)
print(df.head(8))

# 2b) Exibir as 8 últimas linhas
print("\n2. ÚLTIMAS 8 LINHAS DO DATASET:")
print("-" * 80)
print(df.tail(8))

# 3) Contar o número total de linhas e colunas
print("\n3. DIMENSÕES DO DATASET:")
print("-" * 80)
num_linhas, num_colunas = df.shape
print(f"Total de linhas: {num_linhas}")
print(f"Total de colunas: {num_colunas}")

# 4) Identificar o tipo de cada coluna
print("\n4. TIPOS DE DADOS DE CADA COLUNA:")
print("-" * 80)
print(df.dtypes)

# 5) Explorar e descrever impressões gerais sobre o dataset
print("\n5. IMPRESSÕES GERAIS E ANÁLISE EXPLORATÓRIA:")
print("-" * 80)

print("\nNomes das colunas:")
print(df.columns.tolist())

print("\nInformações gerais do dataset (df.info()):")
print("-" * 80)
df.info()

print("\n\nEstatísticas descritivas das colunas numéricas:")
print("-" * 80)
print(df.describe())

print("\n\nValores faltantes (Missing values):")
print("-" * 80)
missing_values = df.isnull().sum()
missing_percentage = (df.isnull().sum() / len(df)) * 100
missing_df = pd.DataFrame({
    'Coluna': missing_values.index,
    'Valores Faltantes': missing_values.values,
    'Percentual (%)': missing_percentage.values
})
print(missing_df.to_string(index=False))

print("\n\nValores únicos por coluna:")
print("-" * 80)
for coluna in df.columns:
    unique_count = df[coluna].nunique()
    print(f"{coluna}: {unique_count} valores únicos")

print("\n\nAMOSTRA DE DADOS POR COLUNA:")
print("-" * 80)
for coluna in df.columns:
    print(f"\n{coluna}:")
    if df[coluna].dtype == 'object':
        print(f"  Tipo: Categórico (texto)")
        print(f"  Primeiros 5 valores: {df[coluna].head().tolist()}")
    else:
        print(f"  Tipo: Numérico")
        print(f"  Primeiros 5 valores: {df[coluna].head().tolist()}")
        print(f"  Min: {df[coluna].min()}, Max: {df[coluna].max()}")

print("\n" + "=" * 80)
print("FIM DA ANÁLISE EXPLORATÓRIA")
print("=" * 80)
