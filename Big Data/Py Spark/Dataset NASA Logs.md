# Relatório de Análise de Logs da NASA com PySpark

## Introdução

O relatório tem como objetivo descrever a análise realizada sobre os arquivos de log de acessos da NASA. Para isso, foi utilizado o PySpark, explorando especificamente a API de RDDs (Resilient Distributed Datasets). A proposta é compreender como aplicar operações de transformação e ação sobre dados distribuídos, a fim de extrair informações relevantes a partir de grandes volumes de registros de acesso.

A análise se concentrou em tópicos como: identificação de hosts distintos, tratamento de erros HTTP 404, contagem de acessos por dia, páginas mais requisitadas com falha, além da soma total de bytes transferidos. O relatório descreve cada etapa do código, explicando seu funcionamento e destacando boas práticas de programação distribuída.



## Metodologia

Leitura dos Dados

Os arquivos NASA_access_log_Jul95 e NASA_access_log_Aug95 foram carregados como RDDs utilizando o método sc.textFile(). Cada linha dos arquivos corresponde a um registro de acesso. Os RDDs foram armazenados em memória com .cache() para evitar recomputações, visto que eram reutilizados em diversas operações.

Estrutura dos Registros

Cada linha segue o padrão do Common Log Format, contendo informações como host, data, requisição, código de status e bytes transferidos. A extração desses campos foi feita com operações de split(), de forma a isolar tokens específicos:

Host/IP: primeiro token da linha.

Request (URL): parte entre aspas "GET ... HTTP/1.0".

Status: penúltimo token (ex.: 200, 404).

Bytes: último token (ou “-” em caso de ausência).

Data: trecho entre colchetes [...], considerando apenas o dia/mês/ano.



## Resultados da Análise

1. Quantidade de Hosts Distintos

Foi desenvolvida a função obterQtdHosts(rdd), que extrai o host de cada linha, aplica .distinct() e, em seguida, .count(). Assim, obteve-se o número total de clientes únicos que acessaram os servidores da NASA em cada mês.

2. Identificação de Erros 404

Para identificar requisições com falha, criou-se a função codigo404(linha), que verifica se o campo de status é igual a “404”. Os RDDs filtrados (erros404_julho e erros404_agosto) foram mantidos em cache, permitindo reutilização em análises posteriores. A ação .count() revelou o número total de erros 404 em cada mês.

3. Páginas Mais Requisitadas com Erro 404

A função top5_hosts404(rdd) extraiu as URLs de requisições malsucedidas, contabilizando suas ocorrências com map + reduceByKey(add). Após ordenar os resultados em ordem decrescente (sortBy), foi aplicado take(5) para exibir as cinco páginas mais requisitadas que resultaram em erro.

4. Contagem de Erros 404 por Dia

A análise por dia foi realizada extraindo a data de cada linha de erro 404. Em seguida, utilizou-se map + reduceByKey(add) para obter a soma diária. O resultado retornou uma lista de pares (data, quantidade), que permitiu visualizar os dias mais problemáticos em termos de acessos malsucedidos.

5. Quantidade Total de Bytes Transferidos

Foi criada a função quantidade_bytes_acumulados(rdd), responsável por somar o campo de bytes transferidos. O código incluiu tratamento para valores inválidos (“-” ou números negativos), atribuindo zero nesses casos. A agregação foi feita com reduce(add), resultando na soma total de bytes transferidos em cada mês.



## Discussão e Boas Práticas

Durante o desenvolvimento, foram destacadas diferenças fundamentais entre transformações e ações no Spark:

Transformações (como map, filter, reduceByKey) são lazy, ou seja, apenas constroem o plano de execução.

Ações (como count, collect, take, reduce) disparam de fato a execução.


### Algumas boas práticas aplicadas incluem:

Uso de .cache() em RDDs reutilizados.

Emprego de try/except para lidar com linhas malformadas.

Preferência por take() em vez de collect() para resultados amostrais, evitando sobrecarga no driver.


Contudo, também foram identificados pontos de melhoria:

O parsing manual com split() é frágil; regex ou o uso de DataFrames com esquema definido seriam mais robustos.

Para análises temporais mais complexas, converter a data em formato timestamp permitiria uso de funções de janela no Spark SQL.

Evitar .collect() em resultados grandes, priorizando agregações distribuídas ou salvando saídas em arquivos.



## Conclusão

A análise dos logs da NASA demonstrou, na prática, como aplicar operações fundamentais do PySpark sobre RDDs. Foi possível contabilizar hosts distintos, identificar erros 404, localizar URLs mais problemáticas, observar a distribuição de falhas por dia e calcular o total de bytes transferidos.

O trabalho reforçou a importância do entendimento entre transformações e ações, além do impacto de operações como reduceByKey (que envolve shuffle) e do uso adequado de cache() para otimizar o desempenho.

Por fim, a abordagem via RDDs fornece grande controle sobre os dados, sendo útil para manipulação de logs “crus”. Entretanto, para análises mais avançadas, o uso de DataFrames e Spark SQL pode oferecer maior expressividade e robustez.
