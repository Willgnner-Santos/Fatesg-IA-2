Memcached & Python: Projeto de Integração e TTL (Time To Live)
Este repositório contém a implementação e documentação de um projeto de integração do sistema de caching Memcached com a linguagem Python. O objetivo principal foi pesquisar, implementar e comprovar o funcionamento do mecanismo de expiração automática de dados (TTL - Time To Live).

Alunos
Maria Clara Ribeiro Di Bragança

Frederico Lemes Rosa

Objetivo da Atividade
Demonstrar a importância e a funcionalidade do Memcached como uma camada de cache em memória para acelerar aplicações, focando em três pilares:

Integração Funcional: Conectar um cliente Python a um servidor Memcached real.

Manipulação de Dados: Implementar comandos essenciais como SET, GET e DELETE.

Comprovação do TTL: Validar que o Memcached remove automaticamente os dados após um tempo de vida definido.

Stack Tecnológica
Sistema Operacional: Ubuntu (via WSL - Windows Subsystem for Linux)

Servidor de Cache: Memcached

Linguagem de Programação: Python 3

Biblioteca Cliente: python-memcached

Guia de Implementação no WSL (Passo a Passo)
A implementação foi realizada em um ambiente real (Ubuntu WSL) e exigiu a superação de desafios comuns de ambiente.

1. Instalação e Ativação do Servidor Memcached
O servidor foi instalado e ativado no Ubuntu, rodando em daemon na porta padrão (11211).

# 1. Instalar o Memcached
sudo apt update
sudo apt install memcached

# 2. Iniciar o serviço
sudo systemctl start memcached

# 3. Verificar o status (deve retornar 'active (running)')
ps aux | grep memcached

2. Preparação do Ambiente Python (VENV)
Enfrentamos o erro externally-managed-environment ao usar o pip diretamente no sistema. A solução correta foi criar um Ambiente Virtual (venv) para isolar as dependências do projeto.

# 1. Criar e acessar a pasta do projeto
mkdir memcached_project
cd memcached_project

# 2. Criar e Ativar o Ambiente Virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar a biblioteca cliente
pip install python-memcached

3. Scripts de Teste
Dois scripts foram desenvolvidos para comprovar as funcionalidades.

A. memcached_teste_ttl.py (Comprovação do TTL)
Objetivo: Armazenar um valor com TTL de 5 segundos, lê-lo imediatamente e, após 6 segundos (time.sleep), tentar lê-lo novamente para comprovar sua expiração.

Comandos Chave:

# Conexão
mc = memcache.Client(['127.0.0.1:11211'], debug=0) 

# Armazenamento com TTL
mc.set(chave_teste, valor_teste, 5) 

# Pausa para expiração
time.sleep(6) 

# Tentativa de leitura após expiração (retorna None)
valor_expirado = mc.get(chave_teste) 

B. memcached_detalhe.py (Aprofundamento)
Objetivo: Demonstrar as operações de manipulação (SET para criar/atualizar, DELETE para remover) e o TTL em um contexto mais detalhado.

Conclusão e Aprendizados
O projeto demonstrou que a integração do Python com o Memcached é simples e extremamente eficiente.

Principais Vantagens Comprovadas:
Velocidade: Leitura e escrita de dados diretamente na RAM (memória).

TTL (Time To Live): O mecanismo de expiração automática garante que os dados em cache não fiquem obsoletos, sendo a principal prova de conceito do nosso projeto.

Simplicidade: O uso da API da biblioteca python-memcached é intuitivo e direto.

Ganhos Técnicos:
Dominamos a configuração de um servidor de cache real e aprendemos a melhor prática de desenvolvimento Python utilizando Ambientes Virtuais (VENV) para gerenciar as dependências do projeto de forma isolada e segura.