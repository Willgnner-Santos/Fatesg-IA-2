# Projeto de Regressão Linear: Idade vs. Salário

Este projeto é uma atividade acadêmica que investiga uma hipótese simples: **A idade de um funcionário pode prever seu salário?**

Utilizamos um modelo de Regressão Linear Simples para analisar 20 registros de funcionários, mas os resultados mostraram que, para este conjunto de dados, a idade sozinha não é um bom previsor.

## O Modelo e os Resultados

Utilizamos um notebook (`.ipynb`) para:
1.  Conectar a um banco MongoDB local (`mongodb://localhost:27017/`).
2.  Carregar os dados da coleção `startup.funcionarios` em um DataFrame do Pandas.
3.  Treinar um modelo de Regressão Linear (`sklearn.linear_model.LinearRegression`) usando `Idade` para prever `Salário`.

Os resultados do modelo foram estatisticamente fracos:

* **R² (Coeficiente de Determinação): 0.1805**
    * Isso indica que o modelo só consegue explicar 18% da variação dos salários.
* **RMSE (Raiz do Erro Quadrático Médio): R$ 1.960,01**
    * Isso significa que as previsões do modelo erram, em média, quase R$ 2.000,00, o que é um valor muito alto.

## O Que a Análise Visual Revelou?

A análise visual (detalhada no notebook e no PDF de análise) foi essencial para entender *por que* o modelo falhou.

### 1. Conclusões do Gráfico de Dispersão (Idade vs. Salário)

A análise deste gráfico mostrou que a correlação entre idade e salário é muito baixa.

* Os pontos estavam muito espalhados. Por exemplo, funcionários na faixa dos 40-50 anos tinham salários variando de R$ 7.000 a R$ 12.000.
* A linha de regressão (tendência) ficou quase plana, confirmando que a idade não tem um impacto marginal no salário.

### 2. Conclusões do Histograma (Distribuição de Salários)

Esta análise foi a pista mais importante.

* Ela revelou uma alta frequência de funcionários (a maioria) concentrada na faixa de R$ 12.000.
* Isso sugere que a estrutura salarial é padronizada e o fator real que determina o salário é provavelmente o **Cargo** (ex: Gerente), e não a idade.

### 3. Conclusões do Gráfico de Resíduos (Análise do Erro)

Esta análise destacou uma segunda causa para o fracasso:

* **Falta de Dados:** Com apenas 20 registros no total, nosso conjunto de teste (20%) era muito pequeno.
* Com tão poucos dados de teste, a avaliação do modelo não é estatisticamente confiável.

## Conclusão da Análise

1.  **A Idade Não é Determinante:** Para este conjunto de dados, a idade tem um impacto muito baixo na previsão do salário.
2.  **A Variável Oculta:** O verdadeiro fator que explica os salários é, provavelmente, uma variável categórica que não foi usada, como o **Cargo**.
3.  **Ação Recomendada:** Para um modelo útil, seria necessário coletar mais dados e incluir variáveis mais relevantes (Cargo, Setor, Tempo de Experiência).

## 🛠️ Tecnologias Utilizadas

* **Banco de Dados:** MongoDB
* **Análise e Modelagem:** Python
    * `pymongo` (Conexão com DB)
    * `pandas` (Manipulação de dados)
    * `scikit-learn` (Modelo de Regressão Linear)
    * `matplotlib` & `seaborn` (Visualização de dados)

## 🎓 Autoria

* **Discentes:** Frederico Lemes Rosa e Maria Clara Ribeiro Di Bragança
* **Docente:** Willgnner
* **Instituição:** Faculdade de Tecnologia Senai de Desenvolvimento Gerencial - FATESG