import pandas as pd
import numpy as np # Adicionado, embora Pandas cubra a maioria das funções aqui

# ====================================================================
# CONFIGURAÇÃO E CARREGAMENTO DE DADOS
# ====================================================================

# URL do Dataset
DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Passo 1: Carregar os dados originais
df_titanic = pd.read_csv(DATA_URL)

# Configurações de visualização (opcional)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("--- 🚢 Dataset Titanic: Início da Análise ---")
print("\n🔍 Primeiras linhas do dataset original:")
print(df_titanic.head())
print("-" * 50)


# ====================================================================
# LIMPEZA E PRÉ-PROCESSAMENTO (DATA CLEANING)
# ====================================================================

# Cria uma cópia para o DataFrame limpo
df_limpo = df_titanic.copy()

# 1. Identificação e Remoção de Duplicatas
num_duplicatas = df_limpo.duplicated().sum()
if num_duplicatas > 0:
    df_limpo = df_limpo.drop_duplicates().copy()
    print(f"\nNúmero de linhas duplicadas removidas: {num_duplicatas}")
else:
    print(f"\nNenhuma linha duplicada encontrada.")

# 2. Tratamento de Valores Ausentes
print("\nValores ausentes por coluna (antes do tratamento):")
print(df_limpo.isnull().sum())

# Tratamento da coluna 'Age' (idade) com a mediana
mediana_idade = df_limpo['Age'].median()
df_limpo['Age'].fillna(mediana_idade, inplace=True)
print(f"\n✔ 'Age' preenchida com a mediana: {mediana_idade:.2f}")

# Tratamento da coluna 'Embarked' (porto de embarque) com a moda
moda_embarque = df_limpo['Embarked'].mode()[0]
df_limpo['Embarked'].fillna(moda_embarque, inplace=True)
print(f"✔ 'Embarked' preenchida com a moda: {moda_embarque}")

# Para a coluna 'Cabin', indicamos sua ausência
df_limpo['Cabin'].fillna('Missing', inplace=True)
print("✔ 'Cabin' preenchida com 'Missing'.")

print("\nVerificação final de valores ausentes no df_limpo:")
print(df_limpo.isnull().sum())
print("-" * 50)


# ====================================================================
# ANÁLISE EXPLORATÓRIA DE DADOS (EDA) E DESAFIOS
# ====================================================================

# --- DESAFIO 1: Mortalidade na 1ª Classe ---
print("🎯 DESAFIO 1: Mortalidade na 1ª Classe")

# Filtrar a 1ª classe que não sobreviveu (usando df_titanic)
nao_sobreviveu_classe1 = df_titanic[(df_titanic['Pclass'] == 1) & (df_titanic['Survived'] == 0)]
count_nao_sobreviveu_classe1 = len(nao_sobreviveu_classe1)

# Total de passageiros da 1ª classe
total_classe1 = df_titanic[df_titanic['Pclass'] == 1].shape[0]

# Calcular a porcentagem
porcentagem_mortalidade_classe1 = (count_nao_sobreviveu_classe1 / total_classe1) * 100

print(f"Total de passageiros da 1ª classe: {total_classe1}")
print(f"1ª classe que NÃO sobreviveram: {count_nao_sobreviveu_classe1}")
print(f"Taxa de mortalidade na 1ª classe: **{porcentagem_mortalidade_classe1:.2f}%**")
print("-" * 50)

# --- DESAFIO 2: Distribuição por Sexo e Porto de Embarque ---
print("🎯 DESAFIO 2: Passageiros por Sexo e Porto de Embarque")

# Contagem por Sexo e Porto de Embarque (usando df_limpo com 'Embarked' preenchido)
tabela_cruzada_sexo_embarque = pd.crosstab(df_limpo['Sex'], df_limpo['Embarked'])

print("Tabela Cruzada (Sex vs. Embarked - C=Cherbourg, Q=Queenstown, S=Southampton):")
print(tabela_cruzada_sexo_embarque)
print("-" * 50)


# --- DESAFIO 3: Idade Média por Sobrevivência ---
print("🎯 DESAFIO 3: Idade Média por Sobrevivência")

# Idade média por Sobrevivência (usando df_limpo com 'Age' preenchido)
media_idade_por_sobrevivencia = df_limpo.groupby('Survived')['Age'].mean()

print("Média de Idade (0 = Não Sobreviveu, 1 = Sobreviveu):")
print(f"Não Sobreviventes: **{media_idade_por_sobrevivencia[0]:.2f} anos**")
print(f"Sobreviventes: **{media_idade_por_sobrevivencia[1]:.2f} anos**")
print("-" * 50)


# --- FEATURE ENGINEERING: Tamanho da Família (FamilySize) ---
print("⚙️ FEATURE ENGINEERING: Family Size")

# Cria a nova coluna FamilySize = SibSp + Parch + 1 (o próprio passageiro)
df_limpo['FamilySize'] = df_limpo['SibSp'] + df_limpo['Parch'] + 1
print("Nova coluna 'FamilySize' (SibSp + Parch + 1) criada.")

# Calcula a taxa de sobrevivência (média de Survived) para cada tamanho de família
media_sobrevivencia_familia = df_limpo.groupby('FamilySize')['Survived'].mean().sort_values(ascending=False)

print("\nTaxa Média de Sobrevivência por Tamanho da Família:")
print(media_sobrevivencia_familia)
print("-" * 50)


# --- ANÁLISE EXTRA: Impacto da Remoção Extrema (dropna) ---
print("⚠️ ANÁLISE: Impacto da Remoção Extrema (dropna no DF original)")

linhas_originais = df_titanic.shape[0]
df_sem_nan = df_titanic.dropna()
linhas_restantes = df_sem_nan.shape[0]
linhas_perdidas = linhas_originais - linhas_restantes

print(f"Linhas no dataset ORIGINAL: {linhas_originais}")
print(f"Linhas após 'dropna()' (sem nenhum NaN): {linhas_restantes}")
print(f"Linhas perdidas: {linhas_perdidas} ({linhas_perdidas / linhas_originais * 100:.2f}%)")
print("-" * 50)

print("\n--- ✅ Análise Concluída! ---")