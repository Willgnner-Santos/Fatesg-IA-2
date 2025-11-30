# Análise Exploratória de Dados (EDA) e Pré-Processamento do Dataset Titanic

## Visão Geral do Projeto

Este repositório contém o *notebook* principal para a análise exploratória de dados (EDA) e o pré-processamento inicial do famoso dataset do Titanic. O objetivo é inspecionar a qualidade dos dados, responder a desafios estatísticos e preparar o dataset para futuras etapas de Machine Learning (Modelagem Preditiva de Sobrevivência).

O arquivo principal de execução é o **`desafio.ipynb`**.

---

## 💾 Dataset e Dicionário de Variáveis

O dataset utilizado (`titanic.csv`) contém dados de 891 passageiros, incluindo informações socioeconômicas e o resultado de sobrevivência.

| Variável | Nome em PT no Código | Tipo | Descrição |
| :--- | :--- | :--- | :--- |
| PassengerId | `id_passageiro` | Numérico | Identificador único do passageiro. |
| Survived | `sobreviveu` | Categórico (0/1) | **Variável Alvo**. (1=Sim, 0=Não). |
| Pclass | `classe_p` | Categórico (1, 2, 3) | Classe do bilhete (Proxy para Status Socioeconômico). |
| Name | `nome` | String | Nome completo do passageiro. |
| Sex | `sexo` | Categórico | Gênero do passageiro. |
| Age | `idade` | Numérico | Idade em anos (Contém Missing Values). |
| SibSp | `irmao_conjuge` | Numérico | Número de irmãos/cônjuges a bordo. |
| Parch | `pais_filhos` | Numérico | Número de pais/filhos a bordo. |
| Ticket | `bilhete` | String | Número do bilhete. |
| Fare | `tarifa` | Numérico | Tarifa paga. |
| Cabin | `cabine` | String | Número da cabine (Muitos Missing Values). |
| Embarked | `embarque` | Categórico | Porto de embarque (C, Q, S). |

---

## 📈 Desafios Estatísticos e Insights

O `desafio.ipynb` contém a solução para as seguintes questões:

1.  **Análise da 1ª Classe:** Filtragem dos passageiros da Primeira Classe que não sobreviveram e cálculo da sua porcentagem em relação ao total da 1ª Classe.
2.  **Contagens:** Distribuição de passageiros por `sexo` e porto de `embarque`.
3.  **Média de Idade:** Cálculo da `idade` média para os grupos de Sobreviventes (1) e Não Sobreviventes (0).
4.  **Análise Bivariada:** Cruzamento da taxa de sobrevivência em relação ao `sexo` e `classe_p`, confirmando que **Mulheres** e passageiros da **1ª Classe** tiveram chances de sobrevivência significativamente maiores.

---

## 🛠️ Pipeline de Pré-Processamento (Passos Concluídos)

A seguinte rotina de limpeza e preparação de dados foi aplicada no *notebook* para tratar os valores ausentes (`NaN`) e preparar o dataset para modelagem:

| Coluna | Ação Realizada | Justificativa |
| :--- | :--- | :--- |
| `cabine` | **Remoção** da coluna. | Excesso de valores ausentes (mais de 77%). |
| `idade` | **Imputação com a Mediana.** | A mediana é mais robusta que a média para manter a distribuição da idade, evitando distorção por *outliers*. |
| `embarque` | **Imputação com a Moda.** | Preenche os poucos valores faltantes (2 NaNs) com o valor mais frequente (Porto 'S'). |
| `sexo`, `embarque` | **Codificação One-Hot.** | Transforma variáveis categóricas em colunas binárias (0 ou 1), essenciais para o treinamento de modelos de Machine Learning. |

---

## 🚀 Como Executar o Desafio

1.  **Abra o Google Colab** e crie um novo *notebook*.
2.  **Faça o Upload** do arquivo `titanic.csv` para o diretório `/content/`.
3.  **Copie e Cole** o conteúdo completo do `desafio.ipynb` nas células e **execute-as em ordem**.