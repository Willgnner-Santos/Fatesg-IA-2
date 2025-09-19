# Processo de Análise de Dados com MapReduce: Um Estudo de Caso

Este documento detalha a metodologia empregada para executar um job de **contagem de palavras** utilizando o framework **MapReduce** em um ambiente **Hadoop**. O objetivo foi processar um arquivo de texto para quantificar a frequência de cada palavra, demonstrando a pipeline completa, desde a preparação do ambiente até a análise dos resultados.

## Metodologia e Execução

O trabalho foi conduzido em um cluster Hadoop, acessado via **SSH** através do **Mobaxterm**. As etapas seguiram uma progressão lógica, visando a clareza e a reprodutibilidade do processo.

### 1. Configuração do Ambiente HDFS

A primeira ação foi a criação de um diretório de trabalho no **Hadoop Distributed File System (HDFS)**. Utilizei o comando `hdfs dfs -mkdir /meuteste` para estabelecer um espaço dedicado ao projeto. A confirmação da criação do diretório foi verificada tanto na linha de comando, quanto na interface web do **Ambari**, assegurando a correta alocação de recursos.

### 2. Ingestão de Dados

O arquivo de entrada, nomeado `meu_arquivo.txt`, foi transferido do sistema de arquivos local para o HDFS. O comando `hdfs dfs -put [caminho_local]/meu_arquivo.txt /meuteste/` foi empregado para a ingestão. A validação da transferência foi realizada em duas frentes:
* **Linha de Comando:** Execução de `hdfs dfs -ls /meuteste` para listar o conteúdo do diretório de destino.
* **Interface Gráfica:** Inspeção visual do diretório `/meuteste` no Ambari, que confirmou a presença do arquivo.

O conteúdo do arquivo foi validado através de `hdfs dfs -cat /meuteste/meu_arquivo.txt`, que revelou o texto a ser processado.

### 3. Execução do Job MapReduce

O cerne da operação consistiu na execução do job **WordCount**. Para isso, foi utilizada a biblioteca de exemplos `hadoop-mapreduce-examples.jar`, uma ferramenta padrão para demonstrações do framework. O comando executado foi:

`hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar wordcount /meuteste/meu_arquivo.txt /meuteste/output_wc`

* `hadoop jar`: Inicia a JVM para execução do job.
* `wordcount`: Invoca a classe principal do programa de contagem de palavras.
* `/meuteste/meu_arquivo.txt`: Define o **caminho de entrada** no HDFS.
* `/meuteste/output_wc`: Define o **caminho de saída** no HDFS, onde o resultado será armazenado.

A saída da execução forneceu métricas detalhadas sobre o job, incluindo contadores de mapeamento e redução, confirmando o sucesso da operação.

### 4. Análise dos Resultados

Com a conclusão do job, a análise dos resultados foi focada no diretório de saída. Primeiramente, o comando `hdfs dfs -ls /meuteste/output_wc` foi utilizado para listar os arquivos gerados. A presença do arquivo `part-r-00000` indicou a conclusão bem-sucedida do processo de redução.

Finalmente, para inspecionar o resultado, o conteúdo do arquivo foi visualizado com `hdfs dfs -cat /meuteste/output_wc/part-r-00000`. O resultado apresentado foi uma lista de palavras únicas e suas respectivas contagens, confirmando o processamento correto do arquivo de entrada. A estrutura do diretório de saída também foi validada através da interface do Ambari.