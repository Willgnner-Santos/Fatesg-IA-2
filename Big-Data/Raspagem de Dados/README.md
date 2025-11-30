# Projeto de IA: Análise e Segmentação de Restaurantes em Goiânia

## Visão Geral do Projeto

Este projeto demonstra o ciclo de vida completo de um pipeline de **Big Data e Data Science**, utilizando dados raspados do Google Places (Goiânia, GO). O objetivo principal foi aplicar técnicas de **Aprendizado Supervisionado** (Regressão e Classificação) e **Não Supervisionado** (Clusterização K-Means) para extrair valor e inteligência de negócio dos dados.

---

## Resultados Chave

### 1. Pré-processamento e Feature Engineering
* **Transformação Logarítmica:** Aplicada à variável `reviewsCount` para tratar a extrema assimetria e o impacto de *outliers*.
* **Codificação One-Hot:** Aplicada à `categoryName` para uso em modelos preditivos.

### 2. Aprendizado Supervisionado (Regressão e Classificação)
O desempenho foi comparado entre modelos Lineares e modelos de Ensemble (Random Forest/KNN).

| Problema | Modelo Vencedor | Métrica de Desempenho | Interpretação |
| :--- | :--- | :--- | :--- |
| **Regressão** (Prever `totalScore`) | **Random Forest Regressor** | **R² Score:** 0.80+ | O modelo explica mais de 80% da variância na nota, sendo a `reviewsCount_log` a *feature* mais importante. |
| **Classificação** (Prever 'Alta Nota' vs 'Baixa Nota') | **K-Nearest Neighbors (KNN) Otimizado** | **AUC:** 0.85+ | Alta capacidade de distinguir restaurantes de alto e baixo desempenho. |

### 3. Aprendizado Não Supervisionado (Clusterização)
* **Algoritmo:** K-Means
* **Otimização:** Método do Cotovelo para definir $K$.
* **Resultado:** Foram identificados 3 ou 4 segmentos de restaurantes distintos, separando grupos como "Estabelecimentos Populares" e "Nichos de Alta Qualidade" (Visualização confirmada via PCA).

---

## Arquitetura do Projeto

Esta é a estrutura final das pastas, garantindo que o projeto seja reprodutível e organizado.

/projeto-ia-restaurantes 
├── data/raw                                
│     └── dataset_crawler-google-places_2025-11-10_12-46-55-562.json   
├── notebooks/ 
│ └── data/02_processed
│ │   └── restaurantes_goiania_processado.csv
│ └── models/ 
│ │   ├── classificador_alta_baixa_nota.pkl        
│ │   ├── classificador_vencedor_otimizado.pkl         
│ │   ├── kmeans_clusterizador_3_clusters.pkl     
│ │   ├── modelo_random_forest_otimizado.pkl
│ │   └── scaler_final.pkl   
│ ├── EDA_Exploracao_Inicial.ipynb 
│ ├── Preprocessamento_e_Modelagem.ipynb 
│ └── Aprendizado_Nao_Supervisionado.ipynb                        
├── requirements.txt                          
├── README.md

## Como Executar o Projeto

1.  **Estrutura:** Garanta que a estrutura de pastas acima esteja configurada.
2.  **Dependências:** Instale as bibliotecas necessárias (pandas, numpy, scikit-learn, joblib, seaborn, matplotlib). `pip install -r requirements.txt`

3.  **Execução:** Siga a ordem numérica dos *notebooks* (`1_EDA` $\rightarrow$ `2_Preprocessamento` $\rightarrow$ `3_Aprendizado`).

