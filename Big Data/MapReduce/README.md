# Exercício Prático de MapReduce: WordCount

Este repositório documenta a execução de um exercício prático para demonstrar o funcionamento do MapReduce, o modelo de programação fundamental do ecossistema Hadoop. A atividade consiste em executar o clássico exemplo **"WordCount"** para contar a ocorrência de cada palavra em um arquivo de texto.

## Ambiente de Execução

O exercício foi realizado utilizando o Hortonworks Data Platform (HDP) Sandbox.

Uma observação importante é que o tutorial sugere o uso do client **MobaXterm**, que é uma ferramenta para Windows. Como esta atividade foi executada a partir de um sistema operacional Linux, a conexão via SSH com o sandbox foi realizada utilizando o terminal **Snowflake**, conforme evidenciado nas capturas de tela.

## Passos Executados

O processo seguiu o roteiro fornecido, desde a criação de um diretório no HDFS até a verificação do resultado final.

### 1. Criação de Diretório no HDFS

Inicialmente, um diretório chamado `meuteste` foi criado no HDFS para armazenar os arquivos de entrada e saída. A criação foi confirmada através da interface do Ambari, como mostra a imagem `ambari.png`.

hdfs dfs -mkdir /meuteste


### 2. Upload do Arquivo de Entrada

Um arquivo de texto foi coletado e inserido no diretório `/meuteste` através do **Files View** no Ambari.

### 3. Verificação do Arquivo no HDFS

O comando abaixo foi utilizado para listar o conteúdo do diretório e confirmar que o arquivo foi carregado com sucesso:

hdfs dfs -ls /meuteste


### 4. Leitura do Conteúdo

Para inspecionar o conteúdo do arquivo de entrada diretamente do HDFS, foi utilizado o comando:

hdfs dfs -cat /meuteste/Bike.txt


### 5. Execução do Job MapReduce (WordCount)

O job WordCount pré-compilado do Hadoop foi executado, especificando o arquivo de texto como entrada (`input`) e um novo diretório (`output_wc`) para o resultado (`output`):

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar wordcount /meuteste/Bike.txt /meuteste/output_wc


### 6. Verificação da Saída

Após a execução do job, o diretório de saída foi listado para verificar se o processamento foi concluído. Conforme esperado, foram gerados os arquivos `_SUCCESS` e `part-r-00000`.

### 7. Visualização do Resultado

Finalmente, o resultado do WordCount foi exibido lendo o conteúdo do arquivo de saída `part-r-00000`:

hdfs dfs -cat /meuteste/output_wc/part-r-00000


## Resultados

A imagem `ssh.png` comprova a execução bem-sucedida de todas as etapas via linha de comando. Ela exibe os contadores do job MapReduce, a verificação dos arquivos de saída e, mais importante, o resultado final da contagem de palavras.

A saída mostra cada palavra seguida pelo número de vezes que ela apareceu no texto, confirmando que o paradigma MapReduce funcionou como esperado.
