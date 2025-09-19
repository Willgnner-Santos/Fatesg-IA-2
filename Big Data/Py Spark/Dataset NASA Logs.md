# Py Spark - NASA Logs
  Os dados são carregados no Spark como RDDs, que são estruturas distribuídas que permitem manipular grandes volumes de informação. A partir desses RDDs, o código aplica várias transformações e ações para explorar os registros.

  Uma das primeiras análises feitas é a contagem da quantidade total de registros, que serve para ter uma noção do tamanho do dataset. Em seguida, o código identifica os hosts, que representam os computadores ou IPs que realizaram acessos, e conta quantas vezes cada um aparece, permitindo descobrir quais foram os que mais acessaram o servidor. Outra análise importante é a listagem das páginas mais requisitadas, mostrando aquelas que tiveram maior número de acessos.

  O código também se preocupa em verificar erros nos acessos, principalmente os do tipo 404, que indicam quando um usuário tentou acessar uma página inexistente. Além disso, há filtros que organizam os acessos por datas, possibilitando observar quantos ocorreram em dias específicos.

  Depois dessas análises com RDDs, o código mostra como as mesmas tarefas podem ser feitas com DataFrames, que são estruturas de mais alto nível no Spark. A vantagem dos DataFrames é que eles permitem escrever consultas de forma mais simples e próxima de SQL, usando operações como groupBy, count e orderBy, enquanto nos RDDs é necessário trabalhar com funções como map e reduceByKey, o que demanda mais código.

  De forma geral, o que eu entendi é que os códigos têm como objetivo transformar os logs brutos da NASA em informações úteis, como a quantidade de acessos, os erros encontrados, os hosts mais ativos e as páginas mais populares. Além disso, o trabalho mostra a diferença entre duas formas de manipular dados no Spark: RDDs, que dão mais controle mas exigem mais esforço, e DataFrames, que simplificam bastante as consultas.
