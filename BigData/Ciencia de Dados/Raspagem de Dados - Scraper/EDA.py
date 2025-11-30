import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("Bibliotecas importadas com sucesso!")

# Carregar o arquivo JSON
try:
    with open('dataset_crawler-google-places_2025-11-29_21-56-40-394.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print(f"Dataset carregado com sucesso!")
    print(f"🔹 Shape: {df.shape[0]} linhas x {df.shape[1]} colunas")
    print(f"🔹 Colunas: {list(df.columns)}\n")

except json.JSONDecodeError as e:
    print(f"ERRO: Arquivo JSON inválido!")
    print(f"   Detalhes: {e}")
    exit()

print("=" * 80)
print("🔹 INFORMAÇÕES BÁSICAS DO DATASET:\n")
df.info()

print("\n🔹 Primeiras 5 linhas:")
print(df.head())

print("\n🔹 Últimas 5 linhas:")
print(df.tail())

print("\n🔹 Valores nulos por coluna:")
print(df.isnull().sum())

print("\n" + "=" * 80)
print("ESTATÍSTICAS DESCRITIVAS - VARIÁVEIS NUMÉRICAS\n")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if len(numeric_cols) > 0:
    print(df[numeric_cols].describe())

    print("\nInformações adicionais:\n")
    for col in numeric_cols:
        if df[col].notna().sum() > 0:
            print(f"• Coluna '{col}':")
            print(f"  - Mediana: {df[col].median():.2f}")
            print(f"  - Desvio padrão: {df[col].std():.2f}")
            if len(df[col].mode()) > 0:
                print(f"  - Moda: {df[col].mode().values[0]:.1f}")
            print()
else:
    print("Nenhuma coluna numérica encontrada!")

print("=" * 80)
print("DISTRIBUIÇÃO POR CATEGORIA:\n")
print(df['categoryName'].value_counts())

print("\nDISTRIBUIÇÃO POR CIDADE:\n")
print(df['city'].value_counts())

print("\nDISTRIBUIÇÃO POR ESTADO:\n")
print(df['state'].value_counts())

print("\nANÁLISE DE COMPLETUDE DOS DADOS:\n")
print(f"Registros com website: {df['website'].notna().sum()} ({df['website'].notna().sum()/len(df)*100:.1f}%)")
print(f"Registros com telefone: {df['phone'].notna().sum()} ({df['phone'].notna().sum()/len(df)*100:.1f}%)")
print(f"Registros com endereço: {df['street'].notna().sum()} ({df['street'].notna().sum()/len(df)*100:.1f}%)")
print(f"Registros com score: {df['totalScore'].notna().sum()} ({df['totalScore'].notna().sum()/len(df)*100:.1f}%)")

print("\n" + "=" * 80)
print("DETECÇÃO DE OUTLIERS - MÉTODO IQR\n")

def detect_outliers_iqr(df, column):
    """
    Detecta outliers usando o método IQR (Interquartile Range)
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    return outliers, lower_bound, upper_bound

if 'totalScore' in df.columns and df['totalScore'].notna().sum() > 0:
    print("OUTLIERS em 'totalScore':\n")
    outliers_score, lb_score, ub_score = detect_outliers_iqr(df, 'totalScore')
    print(f"• Limite inferior: {lb_score:.2f}")
    print(f"• Limite superior: {ub_score:.2f}")
    print(f"• Quantidade de outliers: {len(outliers_score)}")

if 'reviewsCount' in df.columns and df['reviewsCount'].notna().sum() > 0:
    print("\nOUTLIERS em 'reviewsCount':\n")
    outliers_reviews, lb_reviews, ub_reviews = detect_outliers_iqr(df, 'reviewsCount')
    print(f"• Limite inferior: {lb_reviews:.1f}")
    print(f"• Limite superior: {ub_reviews:.1f}")
    print(f"• Quantidade de outliers: {len(outliers_reviews)}")
    
    if len(outliers_reviews) > 0:
        print("\nTop 10 registros com mais reviews (outliers):")
        print(outliers_reviews.nlargest(10, 'reviewsCount')[['title', 'totalScore', 'reviewsCount']])

print("\n" + "=" * 80)
print("GERANDO VISUALIZAÇÕES...\n")

if 'totalScore' in df.columns and df['totalScore'].notna().sum() > 0:
    plt.figure(figsize=(10, 5))
    plt.hist(df['totalScore'].dropna(), bins=15, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Total Score', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.title('Distribuição de Total Score', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.axvline(df['totalScore'].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {df["totalScore"].mean():.2f}')
    plt.axvline(df['totalScore'].median(), color='green', linestyle='--', linewidth=2, label=f'Mediana: {df["totalScore"].median():.2f}')
    plt.legend()
    plt.tight_layout()
    plt.show()

if 'reviewsCount' in df.columns and df['reviewsCount'].notna().sum() > 0:
    plt.figure(figsize=(10, 5))
    sns.histplot(data=df, x='reviewsCount', bins=20, kde=True, color='coral')
    plt.xlabel('Número de Avaliações', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.title('Distribuição de Reviews Count', fontsize=14, fontweight='bold')
    plt.axvline(df['reviewsCount'].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {df["reviewsCount"].mean():.1f}')
    plt.axvline(df['reviewsCount'].median(), color='green', linestyle='--', linewidth=2, label=f'Mediana: {df["reviewsCount"].median():.1f}')
    plt.legend()
    plt.tight_layout()
    plt.show()

if 'totalScore' in df.columns and df['totalScore'].notna().sum() > 0:
    plt.figure(figsize=(8, 6))
    box = plt.boxplot(df['totalScore'].dropna(), vert=True, patch_artist=True,
                      boxprops=dict(facecolor='lightblue', alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      whiskerprops=dict(linewidth=1.5),
                      capprops=dict(linewidth=1.5))
    plt.ylabel('Total Score', fontsize=12)
    plt.title('Boxplot de Total Score', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

if 'reviewsCount' in df.columns and df['reviewsCount'].notna().sum() > 0:
    plt.figure(figsize=(8, 6))
    sns.boxplot(y=df['reviewsCount'], color='salmon')
    plt.ylabel('Número de Avaliações', fontsize=12)
    plt.title('Boxplot de Reviews Count', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

if 'totalScore' in df.columns and 'reviewsCount' in df.columns and df['totalScore'].notna().sum() > 0 and df['reviewsCount'].notna().sum() > 0:
    plt.figure(figsize=(10, 6))
    plt.scatter(df['reviewsCount'], df['totalScore'], alpha=0.6, c='purple', s=100, edgecolors='black', linewidth=0.5)
    plt.xlabel('Número de Avaliações', fontsize=12)
    plt.ylabel('Total Score', fontsize=12)
    plt.title('Relação entre Score e Reviews', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if 'reviewsCount' in df.columns and df['reviewsCount'].notna().sum() > 0:
    plt.figure(figsize=(12, 6))
    top10 = df.nlargest(10, 'reviewsCount')[['title', 'reviewsCount']].sort_values('reviewsCount')
    plt.barh(range(len(top10)), top10['reviewsCount'].values, color='teal', edgecolor='black')
    plt.yticks(range(len(top10)), top10['title'].values, fontsize=10)
    plt.xlabel('Número de Avaliações', fontsize=12)
    plt.title('Top 10 por Número de Reviews', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.show()

if 'categoryName' in df.columns:
    plt.figure(figsize=(10, 8))
    category_counts = df['categoryName'].value_counts()
    colors = sns.color_palette('pastel')[0:len(category_counts)]
    plt.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%',
            startangle=90, colors=colors, textprops={'fontsize': 10})
    plt.title('Distribuição por Categoria', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

print("\nAnálise concluída com sucesso!")