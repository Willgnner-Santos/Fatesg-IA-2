# Documentação - Execução de MapReduce com Hadoop WordCount

## Objetivo
Esta documentação demonstra como executar um job MapReduce usando o exemplo WordCount do Hadoop em um ambiente de desenvolvimento com Hortonworks Sandbox.

## Passos Executados

### 1. Configuração Inicial do Ambiente
- Inicialização da máquina virtual com Hortonworks Sandbox
- Acesso ao servidor via SSH usando MobaXterm
- Verificação da disponibilidade dos serviços Hadoop através do Ambari (interface web)

### 2. Criação da Estrutura de Diretórios no HDFS

Conectado via SSH, execute o comando para criar o diretório de trabalho:

```bash
hdfs dfs -mkdir /testeMapR
```

**Resultado esperado:** Criação do diretório `/testeMapR` no sistema de arquivos distribuído HDFS.

### 3. Preparação do Arquivo de Dados

No terminal local (Arch Linux), foram executados os seguintes comandos para criar o arquivo de teste:

```bash
touch BigData.txt
nano BigData.txt
```

O arquivo `BigData.txt` foi criado e editado contendo dados de exemplo para processamento.

### 4. Upload do Arquivo para o HDFS

**Opção 1 - Via Interface Web (Files View):**
- Acessar a interface web do Ambari
- Navegar para **Files View → user → maria_dev**
- Localizar a pasta `/testeMapR` criada anteriormente
- Fazer upload do arquivo `BigData.txt`

**Opção 2 - Via linha de comando:**
```bash
hdfs dfs -put BigData.txt /testeMapR/
```

### 5. Verificação do Upload

Confirme que o arquivo foi carregado corretamente:

```bash
hdfs dfs -ls /testeMapR
```

**Saída obtida:**
```
Found 1 items
-rw-r--r--   1 maria_dev hdfs   38 2025-09-20 21:52 /testeMapR/BigData.txt
```

### 6. Visualização do Conteúdo do Arquivo

Para verificar o conteúdo do arquivo no HDFS:

```bash
hdfs dfs -cat /testeMapR/BigData.txt
```

### 7. Execução do Job MapReduce (WordCount)

Execute o exemplo WordCount fornecido pelo Hadoop:

```bash
hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-examples.jar wordcount /testeMapR/BigData.txt /testeMapR/output_wc
```

**Parâmetros do comando:**
- `wordcount`: Programa MapReduce para contagem de palavras
- `/testeMapR/BigData.txt`: Arquivo de entrada
- `/testeMapR/output_wc`: Diretório de saída dos resultados

### 8. Verificação dos Resultados

Liste os arquivos de saída gerados:

```bash
hdfs dfs -ls /testeMapR/output_wc
```

**Saída obtida:**
```
Found 2 items
-rw-r--r--   1 maria_dev hdfs   0 2025-09-20 21:55 /testeMapR/output_wc/_SUCCESS
-rw-r--r--   1 maria_dev hdfs   52 2025-09-20 21:55 /testeMapR/output_wc/part-r-00000
```

### 9. Visualização dos Resultados Finais

Examine o resultado da contagem de palavras:

```bash
hdfs dfs -cat /testeMapR/output_wc/part-r-00000 | head
```

**Resultados obtidos:**
```
Map     1
Reduce///   1
a       1
de      1
para    1
tarefa  1
teste   1
```

## Explicação do Processo MapReduce

### Fase Map
- Cada linha do arquivo de entrada é processada
- As palavras são extraídas e emitidas com contagem inicial de 1

### Fase Reduce
- Todas as ocorrências de cada palavra são agrupadas
- A contagem final de cada palavra é calculada

## Arquivos Gerados

1. **`_SUCCESS`**: Indica que o job foi executado com sucesso
2. **`part-r-00000`**: Contém os resultados da contagem de palavras

## Considerações Técnicas

- O job MapReduce foi executado no cluster Hadoop configurado no Hortonworks Sandbox
- Os dados foram processados de forma distribuída, mesmo em ambiente de desenvolvimento
- O resultado mostra cada palavra única encontrada no arquivo com sua respectiva contagem
