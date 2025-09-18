Subindo uma Aplicação Flask com Docker e Docker Compose
Olá! Este projeto é parte de uma atividade de graduação em Inteligência Artificial com foco em Bancos de Dados Não Relacionais. O objetivo aqui foi pegar uma aplicação simples em Python com o framework Flask, empacotá-la em um container Docker e orquestrar sua execução usando o Docker Compose.

O exercício me permitiu explorar como o Docker pode ser usado para criar ambientes isolados e reproduzíveis, o que é fundamental para o desenvolvimento e implantação de aplicações.

Tecnologias Utilizadas
Python: A linguagem de programação da aplicação.

Flask: Um micro-framework para a criação da API web.

Docker: Para criar a imagem e o container da aplicação.

Docker Compose: Para gerenciar a construção e a execução do container de forma simplificada.

Estrutura do Projeto
O projeto é bem simples e direto. Os arquivos principais são:

app.py: O código-fonte da aplicação Flask, que retorna uma mensagem simples em HTML.

requirements.txt: Lista a única dependência da aplicação, o Flask.

Dockerfile: Contém as instruções para construir a imagem Docker do projeto.

docker-compose.yml: Arquivo de configuração para o Docker Compose, definindo como o serviço web deve ser construído e executado.

Como Executar a Aplicação
Para rodar este projeto, você precisa ter o Docker e o Docker Compose instalados na sua máquina.

Clone o Repositório:

Bash

git clone https://www.dio.me/articles/enviando-seu-projeto-para-o-github
cd [pasta do projeto]
Suba os Containers:
Basta executar o comando abaixo. O Docker Compose lerá o arquivo docker-compose.yml, construirá a imagem e iniciará o container em segundo plano.

Bash

docker compose up -d
Acesse a Aplicação:
Após o comando ser executado, a aplicação estará disponível no seu navegador. Acesse o seguinte endereço para ver a mensagem de "Olá, mundo do Docker!":
http://127.0.0.1:5000

Comandos Úteis do Docker Compose
Para ver os logs do serviço:

Bash

docker compose logs -f
Para derrubar os containers e remover a rede:

Bash

docker compose down
Espero que esta documentação ajude a mostrar como a atividade foi realizada e como a aplicação pode ser executada facilmente.
