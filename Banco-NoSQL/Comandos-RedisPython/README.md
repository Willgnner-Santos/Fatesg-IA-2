Comandos Redis com Python (Demonstração de Performance e Estruturas de Dados)
Este repositório contém um script Python que demonstra as principais características do Redis (Remote Dictionary Server), utilizando a biblioteca redis-py. O objetivo é ilustrar a alta performance (baixa latência), a escalabilidade e a flexibilidade do Redis para diferentes tipos de dados.

Estrutura do Projeto
.
├── Comandos Redis - Python.docx        # Documento original do exercício (opcional)
├── python_redis_demo.py              # Script principal com os comandos Redis
└── README.md                         # Este arquivo
Pré-requisitos
Para rodar este script, você precisa ter o Python instalado e um servidor Redis ativo.

1. Servidor Redis
O script se conecta ao servidor padrão localhost:6379.

No Windows (Recomendado): Utilize o Memurai Developer Edition, um port nativo e compatível com o Redis para Windows.

Em Qualquer OS (Mais Robusto): Utilize o Redis Server rodando via Docker ou WSL (Windows Subsystem for Linux).

2. Biblioteca Python
Instale o cliente Python para Redis (redis-py):

Bash

pip install redis
Como Executar o Script
1. Certifique-se de que o Servidor Redis está Ativo
Antes de executar, verifique se o serviço Memurai (ou Redis) está em execução na porta 6379.

2. Execute o Arquivo Python
No seu terminal, navegue até a pasta do projeto e execute:

Bash

python python_redis_demo.py
Análise do Código e Resultados
O script está dividido em quatro seções principais que demonstram os pontos fortes do Redis.

1. Alto Desempenho / Baixa Latência (Testes Iniciais)
Esta seção mede o tempo que o Redis leva para executar um comando simples SET (gravar) e GET (ler). Os resultados demonstram latência extremamente baixa, geralmente na faixa de microssegundos ou milissegundos.

Comandos Utilizados:

redis_client.set("chave", "valor")

redis_client.get("chave")

2. Escalabilidade (Teste de Carga)
Esta seção simula a gravação de 1.000.000 (um milhão) de pares chave/valor sequenciais. O objetivo é demonstrar como o Redis mantém a consistência e a velocidade de acesso mesmo com uma base de dados crescente.

Comandos Utilizados:

redis_client.set(f"chave_{i}", f"valor_{i}") (Em loop)

redis_client.get('chave_500') (Acesso a um item aleatório)

3. Flexibilidade (Estruturas de Dados)
O Redis não é apenas um cache de strings; ele suporta diversas estruturas de dados que são testadas nesta seção:

Estrutura de Dados	Descrição	Comandos Utilizados
String	Armazenamento de texto simples.	SET, GET
Lista	Coleção ordenada de strings.	RPUSH (adicionar ao final), LRANGE (obter a lista completa)
Hash	Estrutura de mapa/dicionário (semelhante a um objeto JSON).	HSET (definir campos), HGETALL (obter todos os campos e valores)
Binário	Armazenamento de dados não textuais (simulado com Base64).	SET, GET

Exportar para as Planilhas
4. Baixa Latência (Uso como Cache)
Esta seção simula 5 acessos sequenciais e repetidos a um item de "cache" (configuracao_cache). O resultado esperado é que todos os 5 acessos sejam executados em um tempo extremamente baixo e consistente, provando a eficácia do Redis como camada de cache.

Comandos Utilizados:

redis_client.set("configuracao_cache", "...")

redis_client.get("configuracao_cache") (Em loop 5 vezes, medindo o tempo a cada acesso)

Limpeza
Para remover todas as chaves criadas durante o teste (principalmente o milhão de chaves), você pode executar o cliente Redis e usar o comando FLUSHDB (ATENÇÃO: Este comando apaga todos os dados da base de dados atual):

PowerShell

# Inicie o cliente CLI do Memurai
memurai-cli

# No prompt do Redis
FLUSHDB