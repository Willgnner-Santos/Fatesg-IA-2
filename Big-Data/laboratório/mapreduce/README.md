# Exercício de MapReduce

Este repositório documenta um exercício prático de MapReduce, focado na contagem de palavras em um arquivo de texto. O processo foi realizado em um ambiente Hadoop e demonstra as etapas de criação de diretórios, upload de arquivos, execução do job MapReduce e visualização dos resultados.

## Meu Caminho de Aprendizagem

Para completar este exercício, segui os passos abaixo, que me permitiram entender o fluxo de trabalho do Hadoop e do MapReduce. As imagens anexadas serviram como base para documentar cada etapa.

### 1. Conexão e Preparação do Ambiente

Inicialmente, conectei-me ao servidor de desenvolvimento usando uma sessão SSH via Mobaxterm. A primeira tela (Prova 1.png) mostra a conexão estabelecida com sucesso.

Em seguida, preparei o ambiente no HDFS para o exercício. Usei o comando `hdfs dfs -mkdir /meuteste` para criar um novo diretório chamado `meuteste` no meu diretório home no HDFS (Prova 2.png e Prova 3.png). Este diretório seria o local de trabalho para o exercício. A criação do diretório também pode ser verificada na interface web do Ambari (Prova 5.png).

### 2. Upload do Arquivo de Dados

Após criar o diretório, foi necessário enviar o arquivo de texto com os dados para o HDFS. O arquivo, chamado `meu_arquivo.txt`, continha o texto que seria processado. Utilizei o comando `hdfs dfs -put [caminho_local]/meu_arquivo.txt /meuteste/` para fazer o upload do arquivo para o diretório `meuteste`.

Para verificar se o arquivo foi carregado com sucesso, executei o comando `hdfs dfs -ls /meuteste`. A saída (Prova 4.png) confirmou que o arquivo estava lá. A interface do Ambari também mostrou a presença do arquivo no diretório `/meuteste` (Prova 6.png).

Em seguida, para inspecionar o conteúdo do arquivo no HDFS, usei o comando `hdfs dfs -cat /meuteste/meu_arquivo.txt`. A saída exibiu o texto do arquivo, que continha informações sobre um simpósio e um artigo, incluindo nomes de professores e áreas de pesquisa (Prova 4.png).

### 3. Execução do Job de MapReduce

A etapa central do exercício foi a execução do job de contagem de palavras. Para isso, usei a ferramenta `hadoop-mapreduce-examples.jar`, que contém implementações de exemplo de MapReduce. O comando completo que executei foi:

`hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar wordcount /meuteste/meu_arquivo.txt /meuteste/output_wc`

* `hadoop jar ...`: Inicia a execução do job.
* `wordcount`: Especifica o job a ser executado, que é a contagem de palavras.
* `/meuteste/meu_arquivo.txt`: Define o arquivo de entrada para o job.
* `/meuteste/output_wc`: Define o diretório de saída onde o resultado será armazenado.

A imagem Prova 7.jpg mostra a saída detalhada da execução do job, indicando que a tarefa foi concluída com sucesso.

### 4. Visualização dos Resultados

Após a conclusão do job, precisei verificar o resultado da contagem de palavras. Primeiramente, listei o conteúdo do diretório de saída com o comando `hdfs dfs -ls /meuteste/output_wc`. A saída (Prova 8.jpg) mostrou os arquivos gerados pelo job, incluindo o arquivo `_SUCCESS` (indicando o sucesso da execução) e o arquivo `part-r-00000`, que contém os dados processados.

Para visualizar o resultado final da contagem de palavras, usei o comando `hdfs dfs -cat /meuteste/output_wc/part-r-00000`. A saída (Prova 9.jpg) exibiu a lista de palavras únicas do texto, cada uma seguida de sua respectiva contagem. Por exemplo, `Artificial` apareceu uma vez, enquanto `Professor` apareceu duas vezes.

A interface web do Ambari também confirmou a criação do diretório de saída `output_wc` e seus respectivos arquivos (Prova 10.jpg), proporcionando uma visão visual do resultado.

Este exercício me permitiu solidificar o conhecimento sobre o ciclo de vida de um job MapReduce em um ambiente Hadoop, desde a preparação dos dados até a análise dos resultados.