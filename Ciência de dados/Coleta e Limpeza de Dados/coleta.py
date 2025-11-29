## 🧪 Kit Prático: Manipulação de Dados com Pandas I
# Tema: Explorando Dados do Titanic
# Ferramenta: Google Colab
# Dataset: https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv

import pandas as pd

# Passo 1: Carregar os dados
df_titanic = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Passo 2: Visualizar as 5 primeiras linhas do dataset
print("\n🔍 Primeiras linhas:")
print(df_titanic.head())

# Passo 3: Verificar o nome das colunas e tipos de dados
print("\n🧾 Informações do DataFrame:")
print(df_titanic.info())

# Estatísticas descritivas para colunas numéricas
print("\nEstatísticas Descritivas para colunas numéricas:")
print(df_titanic.describe())

# Contagem de valores para uma coluna categórica (por exemplo, 'Survived')
print("\nContagem de sobreviventes (0 = Não, 1 = Sim):")
print(df_titanic['Survived'].value_counts())

# Passo 4: Filtrar apenas os passageiros que sobreviveram
sobreviventes = df_titanic[df_titanic['Survived'] == 1]
print("\n🛟 Passageiros que sobreviveram:")
print(sobreviventes.head())

# Passo 5: Criar um novo DataFrame com apenas colunas relevantes
resumo = df_titanic[['Name', 'Sex', 'Age', 'Survived']]
print("\n👤 Resumo com nome, sexo, idade e sobrevivência:")
print(resumo.head())

# Passo 6: Calcular a média de idade dos passageiros
media_idade = df_titanic['Age'].mean()
print(f"\n📊 Média de idade dos passageiros: {media_idade:.2f} anos")

# Passo 7: Filtrar passageiros do sexo feminino com menos de 18 anos
meninas = df_titanic[(df_titanic['Sex'] == 'female') & (df_titanic['Age'] < 18)]
print("\n👧 Passageiras com menos de 18 anos:")
print(meninas[['Name', 'Age']])

tickets = df_titanic['Ticket']
print(f"Tickets {tickets}")


# 1. Identificação e Remoção de Duplicatas
num_duplicatas = df_titanic.duplicated().sum()
if num_duplicatas > 0:
    df_limpo = df_titanic.drop_duplicates().copy()
    print(f"\nNúmero de linhas duplicadas: {num_duplicatas}")
    print(f"Dataset após a remoção de duplicatas. Novas dimensões: {df_limpo.shape}")
else:
    df_limpo = df_titanic.copy()
    print(f"\nNenhuma linha duplicada encontrada.")

# 2. Identificação de Valores Ausentes
print("\nValores ausentes por coluna (antes do tratamento):")
print(df_limpo.isnull().sum())

# 3. Tratamento de Valores Ausentes
# Tratar a coluna 'Age' (idade) com a mediana
mediana_idade = df_limpo['Age'].median()
df_limpo['Age'].fillna(mediana_idade, inplace=True)
print(f"\nValores ausentes na coluna 'Age' preenchidos com a mediana: {mediana_idade:.2f}")

# 4. Tratar a coluna 'Embarked' (porto de embarque) com o valor mais frequente
moda_embarque = df_limpo['Embarked'].mode()[0]
df_limpo['Embarked'].fillna(moda_embarque, inplace=True)
print(f"Valores ausentes na coluna 'Embarked' preenchidos com a moda: {moda_embarque}")

# 5. Para a coluna 'Cabin' (cabine), que tem muitos valores ausentes, vamos apenas indicar sua ausência
df_limpo['Cabin'].fillna('Missing', inplace=True)
print("Valores ausentes na coluna 'Cabin' preenchidos com 'Missing'.")

# 6. Verificação e Salvamento
print("\nVerificação final de valores ausentes:")
print(df_limpo.isnull().sum())