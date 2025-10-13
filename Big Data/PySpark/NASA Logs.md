# Mini-relatório: Análise de Dados usando PySpark


## Compreensão do pipeline

A atividade desenvolvida no Google Colab realiza a análise de dados de logs da NASA utilizando o PySpark.
Inicialmente, o ambiente é configurado com a instalação do Java e do PySpark, que são essenciais para o funcionamento do Apache Spark.
Em seguida, os arquivos compactados com os logs de acessos (Julho e Agosto de 1995) são baixados e extraídos. Cada linha desses arquivos representa uma requisição a um servidor web da NASA.

Após a configuração, os dados são carregados para o PySpark por meio de RDDs (Resilient Distributed Datasets), que permitem o processamento distribuído.
Com isso, é possível executar transformações e ações, como contagem de requisições, identificação de hosts únicos e filtragem de erros.
O projeto demonstra o uso prático de operações como map, filter e reduce, mostrando como o PySpark trata grandes volumes de dados de forma eficiente.

## Impressões sobre o uso do PySpark

O PySpark se mostrou uma ferramenta poderosa para o processamento de dados em larga escala.
Mesmo trabalhando em um ambiente como o Google Colab, foi possível perceber como o Spark distribui as tarefas e executa as operações de forma paralela, o que aumenta a velocidade de análise quando comparado ao processamento tradicional em Python puro.

Apesar de exigir uma certa configuração inicial, o uso das RDDs e das funções do Spark facilita bastante a manipulação de grandes conjuntos de dados.
A principal vantagem observada foi a capacidade de lidar com arquivos grandes e realizar cálculos complexos de forma otimizada.

## Metodologia aplicada

A metodologia aplicada consiste em um fluxo típico de engenharia de dados:

 - Preparação do ambiente,

 - Obtenção dos dados,

 - Limpeza e processamento,

 - Análise e interpretação dos resultados.

Na atividade, os logs foram lidos, convertidos em RDDs e submetidos a transformações que extraem informações relevantes sobre os acessos.
Esse tipo de pipeline é comum em projetos de Big Data, onde o volume de informações exige uma estrutura escalável e ferramentas que permitam o processamento distribuído, como o Apache Spark.

## Conclusão:
Este relatório foi elaborado com base na execução e análise da atividade “Análise de Dados usando PySpark RDD – Dataset NASA Logs Web”, demonstrando compreensão sobre o funcionamento do pipeline e a aplicabilidade do PySpark em análises de grandes volumes de dados.
