# Aplicação do Modelo CRISP-DM no Projeto CogniKids

## 1. Business Understanding (Entendimento do Negócio)
* **Definição do Problema:** Crianças neurodivergentes frequentemente possuem dificuldades em comunicar verbalmente o início de crises de ansiedade. Educadores e responsáveis demoram a perceber os sinais físicos sutis, resultando em intervenções tardias.
* **Objetivo de Data Science:** Desenvolver um sistema preditivo capaz de identificar padrões fisiológicos associados a crises em tempo real. O sistema deve distinguir com precisão entre "Ansiedade" e "Atividade Física" (estados biologicamente semelhantes) para alertar os professores preventivamente.
* **Meta de Sucesso:** Maximizar a segurança do aluno (Recall alto), priorizando a emissão de alertas em situações de dúvida (falsos positivos) em detrimento da omissão de uma crise real (falsos negativos).

## 2. Data Understanding (Entendimento dos Dados)
* **Fonte dos Dados:** Devido a restrições éticas que impedem a indução de estresse em crianças reais para coleta de dados, foi utilizado um Digital Twin (Gêmeo Digital). O script `iot_simulator.py` gera dados estocásticos baseados em "Personas" (ex: Ana Calma, Lucas Ansioso).
* **Variáveis Monitoradas (Features):**
    1. **BPM (Batimentos Cardíacos):** Eleva-se tanto em atividade física quanto em crises de ansiedade.
    2. **GSR (Resposta Galvânica da Pele):** Indicador de condutividade/suor. Tende a ser alto na ansiedade (suor frio) e médio no exercício.
    3. **Movement Score (Acelerômetro):** Variável discriminante crucial. Alto no exercício físico, baixo ou travado durante crises de ansiedade/pânico.
* **Exploração:** A análise preliminar dos dados sintéticos confirmou a sobreposição de faixas de BPM entre os estados "Ativo" e "Tenso", validando a necessidade de um modelo multivariado.

## 3. Data Preparation (Preparação dos Dados)
* **Engenharia de Atributos:** No script `train_model.py`, foram estabelecidas regras fisiológicas (`ESTADOS`) que delimitam as faixas de valores para cada situação (Calmo, Ativo, Tenso, Crise).
* **Simulação de Ruído:** Foi injetado um ruído aleatório de 25% nos dados de treinamento e criada uma sobreposição proposital entre as classes "Ativo" e "Tenso". Isso simula a imprecisão natural de sensores IoT de baixo custo e evita que o modelo aprenda regras perfeitas que falhariam no mundo real.
* **Normalização:** O pipeline garante que os dados brutos recebidos via MQTT sejam padronizados em formato JSON estruturado antes da ingestão pelo modelo.

## 4. Modeling (Modelagem)
* **Algoritmo Selecionado:** Random Forest Classifier (Floresta Aleatória).
* **Justificativa:** Este algoritmo foi escolhido pela sua robustez em lidar com ruídos e outliers, comuns em dados de sensores vestíveis, e pela capacidade de modelar relações não-lineares melhor do que Árvores de Decisão simples ou Regressões Lineares.
* **Treinamento:** O modelo foi treinado utilizando milhares de amostras sintéticas geradas pelas regras fisiológicas definidas na etapa anterior, aprendendo a fronteira de decisão complexa entre "atividade física intensa" e "crise de ansiedade".

## 5. Evaluation (Avaliação)
* **Métricas de Desempenho:** O modelo alcançou uma acurácia realista de aproximadamente 82% nos dados de teste.
* **Análise de Erros:** A análise da Matriz de Confusão indicou que a maioria dos erros ocorre na classificação de estados limítrofes entre "Tenso" e "Ativo".
* **Validação do Negócio:** O comportamento do modelo foi considerado satisfatório para o objetivo de negócio, pois demonstra um viés conservador (Safety-First), garantindo que situações de risco potencial sejam sinalizadas para verificação humana.

## 6. Deployment (Implantação)
* **Arquitetura de Big Data:** O modelo treinado (`model.joblib`) foi implantado em um microserviço Python (`alert_monitor.py`) que opera de forma desacoplada.
* **Fluxo de Execução:**
    1. Os dados são ingeridos via MQTT e armazenados em buffer numa fila Redis.
    2. O worker consome a fila e realiza a inferência em tempo real.
    3. Os dados brutos são persistidos no Data Lake (`iot_raw_data`) no MongoDB.
    4. As predições positivas de crise são gravadas no Data Mart (`alerts`).
* **Consumo:** As informações do Data Mart são consumidas via API e exibidas instantaneamente no Dashboard do Professor, fechando o ciclo de valor.