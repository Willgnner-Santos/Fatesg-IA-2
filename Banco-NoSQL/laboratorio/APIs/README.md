# Minha Jornada de Aprendizado com APIs e FastAPI

---

### Visão Geral do Projeto

Este projeto é o resultado da minha jornada de aprendizado com **FastAPI**, um framework Python moderno e de alto desempenho para construir APIs. A atividade foi dividida em três exercícios que me permitiram entender, na prática, desde os conceitos mais básicos de requisições HTTP até a implementação de um sistema de autenticação simples.

O objetivo principal foi não apenas executar o código, mas também **entender o que está acontecendo** em cada etapa e experimentar as mudanças para observar os efeitos. O projeto é composto por uma **API backend** (construída com FastAPI) e um **cliente frontend simples** (criado com Flask) para interagir com a API de forma visual.

---

### O Caminho da Aprendizagem

#### Passo 1: Subindo a API e Explorando o Básico

Meu primeiro desafio foi colocar a API no ar. Após configurar o ambiente virtual e instalar as dependências, iniciei o servidor e pude ver a resposta da API na rota principal (`/`). A resposta me mostrou um guia para as rotas de documentação (`/docs` e `/redoc`).

A partir da documentação interativa (Swagger UI), comecei a explorar os primeiros endpoints:

* **`GET /api/v1/ping`**: Esse endpoint foi meu "health-check". Usei-o para confirmar que a API estava online e respondendo com a mensagem esperada `{"ok": true, "message": "pong"}`.
* **`POST /api/v1/echo`**: Aqui, entendi como enviar dados no corpo de uma requisição. Eu enviei um nome, e a API me devolveu uma saudação personalizada, o que foi uma ótima maneira de ver a comunicação entre cliente e servidor funcionando.

#### Passo 2: Dominando o CRUD de Tarefas (RESTful)

O segundo exercício foi focado na criação de um **CRUD (Create, Read, Update, Delete)** para um recurso de `tasks`. Os dados são mantidos em memória, então cada vez que o servidor reinicia, as tarefas somem, o que me fez entender a importância de um banco de dados real.

* **`GET /api/v1/tasks`**: Comecei listando as tarefas. Ao acessar a rota, vi que uma tarefa de exemplo (`Estudar APIs`) já estava lá por padrão.
* **`POST /api/v1/tasks`**: Criei uma nova tarefa, enviando o título via requisição. Fiquei atento ao código de status **201 (Created)**, que indica sucesso na criação de um novo recurso, e ao `Location` header que aponta para a URL da nova tarefa.
* **`GET /api/v1/tasks/{task_id}`**: Usei essa rota para buscar uma tarefa específica pelo ID. Essa prática me mostrou como as APIs usam IDs na URL para identificar recursos.
* **`PUT /api/v1/tasks/{task_id}` vs. `PATCH /api/v1/tasks/{task_id}`**: Este foi um ponto crucial de aprendizado. Usei o **`PUT`** para atualizar todos os campos de uma tarefa, e o **`PATCH`** para fazer uma atualização parcial, como apenas mudar o status `done` de `true` para `false` ou vice-versa.
* **`DELETE /api/v1/tasks/{task_id}`**: Por fim, testei a exclusão. A resposta **204 (No Content)** me ensinou que, em requisições de sucesso que não retornam um corpo de dados, esse é o status code ideal.

#### Passo 3: Adicionando Segurança e Autenticação

O último exercício me introduziu ao conceito de autenticação em APIs. A rota `POST /api/v1/auth/login` me permitiu simular um login, onde eu enviava um nome de usuário e uma senha, e a API me retornava um token fixo (`aluno123`).

Com o token em mãos, pude testar as rotas protegidas:

* **`GET /api/v1/secure/tasks`**: Tentar acessar essa rota sem o token resultava em um erro de autorização. Para ter sucesso, eu precisei adicionar o cabeçalho **`Authorization: Bearer aluno123`** à minha requisição.

Essa etapa solidificou meu entendimento sobre como a segurança é aplicada em APIs, garantindo que apenas usuários autorizados possam acessar certas funcionalidades.