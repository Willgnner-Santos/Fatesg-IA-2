# Relatório: Análise de Logs NASA com PySpark RDD

## Introdução

Este trabalho apresenta uma implementação prática de processamento distribuído utilizando Apache Spark através da API RDD (Resilient Distributed Dataset) em Python. O objetivo foi explorar logs históricos de servidores web da NASA para extrair insights relevantes sobre padrões de acesso, erros e utilização de recursos.

## Fundamentação Teórica

### Por que Apache Spark?

O Apache Spark representa uma evolução no processamento de grandes volumes de dados, oferecendo capacidades de computação em memória que superam significativamente frameworks anteriores como MapReduce. A API de RDD, embora considerada de baixo nível comparada aos DataFrames modernos, proporciona controle granular sobre operações distribuídas.

### Conceitos Centrais Aplicados

**Transformações Lazy (Preguiçosas):** Operações como `map()`, `filter()` e `reduceByKey()` não executam imediatamente. O Spark constrói um grafo acíclico direcionado (DAG) de operações, otimizando a execução apenas quando uma ação é invocada.

**Ações:** Métodos como `count()`, `collect()` e `take()` disparam a execução do pipeline de transformações, trazendo resultados para o driver ou agregando-os.

**Resiliência:** RDDs mantêm linhagem (lineage) das transformações, permitindo recomputação automática de partições perdidas em caso de falhas.

**Paralelismo:** Dados são automaticamente particionados e processados em paralelo através de múltiplos núcleos ou nós do cluster.

## Metodologia de Implementação

### Configuração do Ambiente

A preparação do ambiente envolveu:

1. **Instalação do JDK 8:** O Spark executa sobre a JVM (Java Virtual Machine), sendo essencial garantir compatibilidade com a versão correta do Java.

2. **Configuração do PySpark:** Biblioteca Python que fornece interface para o motor Spark, permitindo desenvolvimento em linguagem mais acessível.

3. **Definição do SparkContext:** Ponto de entrada para funcionalidades RDD, configurado para execução local com alocação de 5GB de memória para o executor.

```python
configuracao = (SparkConf()
                .setMaster("local")
                .setAppName("Exercicio Nasa Logs")
                .set("spark.executor.memory", "5g"))
sc = SparkContext(conf=configuracao)
```

### Dataset Utilizado

Os dados consistem em logs reais de servidores HTTP da NASA dos meses de julho e agosto de 1995, disponibilizados publicamente para fins educacionais. Cada registro segue o formato Common Log Format estendido:

```
host - - [timestamp] "método URL protocolo" status bytes
```

**Volume dos dados:**
- Julho: ~1.89 milhões de requisições (~196 MB)
- Agosto: ~1.57 milhões de requisições (~161 MB)

### Pipeline de Processamento

#### 1. Carregamento e Persistência

```python
julho = sc.textFile('aulapython/NASA_access_log_Jul95').cache()
agosto = sc.textFile('aulapython/NASA_access_log_Aug95').cache()
```

O método `cache()` instrui o Spark a manter o RDD em memória após a primeira computação, evitando releituras do disco em operações subsequentes.

#### 2. Extração de Hosts Únicos

Para determinar quantos visitantes distintos acessaram o servidor:

```python
def obterQtdHosts(rdd):
    return rdd.map(lambda line: line.split(' ')[0]) \
              .distinct() \
              .count()
```

Esta operação demonstra o padrão map-reduce: extraímos o IP/hostname (primeiro campo), removemos duplicatas e contamos.

#### 3. Identificação de Erros 404

Implementamos uma função robusta para detectar requisições que resultaram em "Not Found":

```python
def codigo404(linha):
    try:
        codigohttp = linha.split()[-2]  # Penúltimo token = status HTTP
        return codigohttp == '404'
    except:
        return False
```

O tratamento de exceções garante que linhas malformadas não interrompam o processamento.

#### 4. URLs Mais Problemáticas

Identificar as páginas que mais geram erros 404 permite priorizar correções:

```python
def top5_hosts404(rdd):
    urls = rdd.map(lambda linha: linha.split('"')[1].split(' ')[1])
    counts = urls.map(lambda url: (url, 1)).reduceByKey(add)
    return counts.sortBy(lambda par: -par[1]).take(5)
```

**Importância do `reduceByKey()`:** Esta operação realiza agregação local (combiner) antes do shuffle, reduzindo drasticamente a quantidade de dados transferidos entre nós.

#### 5. Distribuição Temporal de Erros

Analisar erros por dia revela padrões e possíveis incidentes:

```python
def contador_dias_404(rdd):
    dias = rdd.map(lambda linha: linha.split('[')[1].split(':')[0])
    return dias.map(lambda dia: (dia, 1)).reduceByKey(add).collect()
```

#### 6. Volume de Transferência

Calcular bytes totais transferidos auxilia em planejamento de capacidade e custos:

```python
def quantidade_bytes_acumulados(rdd):
    def contador(linha):
        try:
            count = int(linha.split(" ")[-1])
            return count if count >= 0 else 0
        except:
            return 0
    return rdd.map(contador).reduce(add)
```

## Resultados Obtidos

### Análise Quantitativa

**Hosts Únicos:**
- Julho: 81.983 visitantes distintos
- Agosto: 75.060 visitantes distintos

Esta métrica indica o alcance do servidor e pode ser correlacionada com campanhas ou eventos específicos.

**Erros HTTP 404:**
- Julho: 10.845 ocorrências
- Agosto: 10.056 ocorrências

Aproximadamente 0,6% das requisições resultaram em erro, o que é aceitável mas indica oportunidades de melhoria.

**Top 5 URLs com 404 (Agosto):**
1. `/pub/winvn/readme.txt` - 1.337 erros
2. `/pub/winvn/release.txt` - 1.185 erros
3. `/shuttle/missions/STS-69/mission-STS-69.html` - 683 erros
4. `/images/nasa-logo.gif` - 319 erros
5. `/shuttle/missions/sts-68/ksc-upclose.gif` - 253 erros

**Volume de Dados:**
- Julho: 38,7 GB transferidos
- Agosto: 26,8 GB transferidos

### Interpretação dos Resultados

Os arquivos de documentação do Windows (winvn) lideram os erros 404, sugerindo links desatualizados em documentações externas ou páginas descontinuadas. Missões específicas do Shuttle também apresentam links quebrados, possivelmente devido a reorganizações de estrutura de diretórios.

O pico de transferência em julho pode estar relacionado ao aniversário do pouso lunar (20 de julho), gerando maior interesse histórico.

## Reflexões sobre a Experiência

### Desafios Encontrados

**Parsing de Dados Semi-estruturados:** Logs apresentam variações sutis que exigem funções defensivas com tratamento de exceções. A abordagem com `split()` é funcional mas frágil; expressões regulares seriam mais robustas.

**Gerenciamento de Memória:** Mesmo com `cache()`, RDDs grandes podem causar problemas de memória. O ajuste de `spark.executor.memory` foi crucial para evitar falhas OOM (Out of Memory).

**Debugging Distribuído:** Erros em transformações lazy só aparecem na execução de ações, dificultando depuração. Testar com `take()` em amostras pequenas foi essencial.

### Vantagens do Paradigma RDD

**Controle Fino:** Diferente de DataFrames, RDDs permitem operações arbitrárias sem imposição de esquema, ideal para dados não estruturados.

**Programação Funcional:** O uso de funções lambda e imutabilidade torna o código mais seguro para paralelismo.

**Escalabilidade Horizontal:** O mesmo código funciona tanto localmente quanto em clusters com centenas de nós, apenas ajustando configurações.

### Limitações Observadas

**Ausência de Otimizações Catalyst:** DataFrames modernos utilizam o otimizador Catalyst e o motor Tungsten, oferecendo performance superior para muitos casos de uso.

**Verbosidade:** Operações que em SQL seriam uma linha exigem múltiplas transformações encadeadas.

**Type Safety:** Python é dinamicamente tipado, aumentando chances de erros em runtime que Scala detectaria em compilação.

## Aplicações Práticas

Este tipo de análise é fundamental em diversos cenários empresariais:

**Monitoramento de SRE (Site Reliability Engineering):** Identificação proativa de problemas antes que afetem usuários em larga escala.

**SEO (Search Engine Optimization):** Links 404 prejudicam ranqueamento; dashboards automatizados podem alertar equipes de conteúdo.

**FinOps:** Análise de bytes transferidos subsidia negociações com CDNs e provedores de cloud, otimizando custos.

**Segurança:** Padrões anômalos de hosts ou requisições podem indicar ataques DDoS ou tentativas de exploração.

**Produto e Marketing:** Entender quais páginas/recursos são mais acessados orienta roadmap de features e campanhas.

## Evolução e Próximos Passos

### Migrando para DataFrames/Spark SQL

```python
df = spark.read.text("logs.txt")
df = df.withColumn("host", regexp_extract("value", r"^(\S+)", 1))
df = df.withColumn("status", regexp_extract("value", r"\s(\d{3})\s", 1))
df.filter(col("status") == "404").groupBy("host").count().show()
```

DataFrames oferecem sintaxe mais declarativa e otimizações automáticas.

### Streaming Real-Time

Integração com Kafka ou AWS Kinesis permitiria análise contínua:

```python
stream = spark.readStream.format("kafka").load()
stream.writeStream.format("console").start()
```

### Machine Learning

Detecção de anomalias com MLlib:

```python
from pyspark.ml.clustering import KMeans
# Agrupar padrões de acesso para identificar comportamentos suspeitos
```

## Conclusão

Esta experiência demonstrou a capacidade do Apache Spark de processar volumes substanciais de dados mesmo em hardware modesto. A API RDD, embora considerada legada, ensina fundamentos essenciais de computação distribuída que se aplicam a qualquer framework moderno.

Os insights extraídos dos logs NASA, apesar de históricos, ilustram problemas reais enfrentados por equipes de engenharia: balanceamento entre disponibilidade, performance e custos. A metodologia aplicada é diretamente transferível para logs de APIs modernas, telemetria IoT, eventos de aplicações e pipelines de dados corporativos.

Compreender transformações lazy, shuffle, particionamento e resiliência através de RDDs fornece base sólida para trabalhar com abstrações de mais alto nível como DataFrames e Datasets, preparando profissionais para desafios reais em engenharia de dados.

---

**Tecnologias Utilizadas:**
- Apache Spark 3.5.1
- PySpark (Python 3.12)
- Java 8 (OpenJDK)
- Google Colab (ambiente de execução)

**Código-fonte:** Disponível no repositório GitHub conforme solicitado.