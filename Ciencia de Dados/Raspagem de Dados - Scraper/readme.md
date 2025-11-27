# 🛒 Inteligência de Mercado: Supermercados em Bela Vista de Goiás

Este projeto foca na análise de competitividade e comportamento do consumidor no setor de supermercados em Bela Vista de Goiás. A análise vai além do básico, utilizando métricas ponderadas e correlações visuais.

## 📊 Sobre o Dataset
Os dados (`dataset_google-maps-extractor...517.json`) contêm informações detalhadas sobre supermercados, incluindo contagem de fotos, avaliações, serviços oferecidos e horários de funcionamento.

## 🚀 Destaques da Análise
Diferente de uma análise padrão, este projeto implementou técnicas avançadas de interpretação de dados:

1.  **Relação Popularidade x Qualidade:** Scatterplot para identificar se mercados mais cheios são necessariamente os melhores.
2.  **Análise de Serviços:** Levantamento de diferenciais competitivos (Acessibilidade, Aceitação de Crédito, Loja Física), ignorando dados óbvios (como "faz entrega").
3.  **Categorias Associadas:** Análise de serviços agregados (ex: Mercados que também são Padarias ou Açougues).
4.  **Engajamento Visual (Combo Chart):** Um gráfico comparativo (Barras + Linha) para validar a hipótese: *"Mercados que postam mais fotos atraem mais avaliações?"*.
5.  **Ranking Ponderado (IMDb Score):** Criação de uma métrica matemática ("Score Ajustado") que penaliza locais com poucas avaliações e destaca os líderes consistentes de mercado.

## 🛠️ Tecnologias
* Python 3.x
* Pandas (Normalização de dados e Cálculos estatísticos)
* Seaborn & Matplotlib (Gráficos avançados e customização de legendas)
* NumPy (Suporte matemático)

## ⚙️ Como Executar
1.  Certifique-se de ter o arquivo `json` na mesma pasta do notebook.
2.  Instale as dependências necessárias:
    ```bash
    pip install pandas matplotlib seaborn numpy
    ```
3.  Execute o notebook para gerar os relatórios visuais e o ranking final.