# 🍽️ Análise Exploratória de Dados: Restaurantes em Goiânia

Este projeto realiza uma Análise Exploratória de Dados (EDA) detalhada sobre um conjunto de dados de restaurantes em Goiânia, extraídos do Google Maps. O objetivo é entender padrões de preço, popularidade e qualidade por localização.

## 📊 Sobre o Dataset
O arquivo utilizado (`dataset_crawler-google-places...107.json`) é um JSON rico contendo dados aninhados (nested dictionaries), incluindo:
- Notas e número de avaliações.
- Informações de Preço (`price`).
- Detalhes aninhados em `additionalInfo` (Serviços, Acessibilidade, etc.).
- Localização (Bairro, Latitude/Longitude).

## 🚀 Técnicas Utilizadas
- **Limpeza de Dados:** Tratamento de caracteres especiais na coluna de preços (remoção de `$` para evitar erros no Matplotlib).
- **Engenharia de Atributos:** Extração de dados de dicionários aninhados e listas.
- **Análise Visual:** Uso de `Seaborn` e `Matplotlib` para gerar insights.

## 📈 Principais Análises
O notebook gera as seguintes visualizações estratégicas:

1.  **Distribuição de Preços:** Análise das faixas de preço mais comuns (Baixo, Médio, Alto).
2.  **Top Categorias:** Identificação dos tipos de culinária predominantes na cidade.
3.  **Qualidade por Bairro (Boxplot):** Comparação da variação de notas entre os principais bairros (Setor Sul, Central, etc.).
4.  **Campeões por Bairro:** Identificação nominal do melhor restaurante de cada região, utilizando critérios de desempate (Nota + Popularidade).

## 🛠️ Tecnologias
* Python 3.x
* Pandas (Manipulação de JSON e DataFrames)
* Seaborn & Matplotlib (Visualização de Dados)

## ⚙️ Como Executar
1.  Certifique-se de ter o arquivo `json` na mesma pasta do notebook.
2.  Instale as dependências:
    ```bash
    pip install pandas matplotlib seaborn
    ```
3.  Execute o Jupyter Notebook célula por célula.