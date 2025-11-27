## Documentação do Exercício: AULA01 - Familiarização e Inspeção de Dados

O notebook **`Manipulacao-Basica-de-Dados.ipynb`** foi dedicado à aplicação das cinco etapas fundamentais para a primeira análise de estrutura de um dataset, utilizando o `movies.csv`.

### Resultados da Análise de Estrutura

Os objetivos do exercício e a metodologia utilizada foram:

| Objetivo | Comando Pandas Utilizado | Análise e Conclusão |
| :--- | :--- | :--- |
| **1. Abertura do Dataset** | `pd.read_csv()` | O arquivo CSV foi carregado com sucesso para um objeto `DataFrame`, pronto para manipulação. |
| **2. Visualização Inicial** | `df.head(8)` e `df.tail(8)` | Confirmação da correta importação e observação dos primeiros e últimos registros para inspecionar o formato dos dados. |
| **3. Determinação da Dimensão** | `df.shape` | Identificação precisa do número total de linhas e colunas, estabelecendo o volume e a dimensionalidade do dataset. |
| **4. Identificação dos Tipos** | `df.dtypes` | Verificação dos tipos de dados de cada coluna (`int64`, `float64`, `object`), essencial para o planejamento do pré-processamento. |
| **5. Exploração Geral** | `df.info()` | Resumo abrangente que revelou a presença de **valores faltantes (NaN)** em diversas colunas (indicado pela contagem de valores não-nulos), sinalizando a necessidade de tratamento de dados para a etapa de limpeza. |

### Principais Aprendizados

* O método `df.info()` é a ferramenta mais eficaz para uma rápida inspeção da qualidade e da estrutura de um DataFrame.
* A correta identificação dos tipos de dados é fundamental para o **Feature Engineering**, indicando a necessidade de codificação para colunas do tipo `object` (texto), como títulos e gêneros.
* A análise de valores ausentes direciona a próxima fase do projeto para a limpeza de dados e a garantia da integridade referencial.

---

**Tecnologias:** Python, Pandas, Google Colab.

**Autor:** Frederico Lemes Rosa