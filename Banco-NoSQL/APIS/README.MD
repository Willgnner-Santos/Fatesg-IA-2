# Documentação: Desenvolvendo uma Aplicação com APIs (FastAPI + Flask)

Este projeto foi o meu espaço para aprender na prática como funcionam as APIs. O objetivo era construir uma API robusta com **FastAPI** e, em seguida, criar uma interface simples de `front-end` usando **Flask** para consumir essa API. Este `README` documenta o meu caminho de aprendizado, os desafios que superei e o resultado final.

---

### Meu Caminho de Aprendizagem

#### 1. A Base: Construindo o Backend com FastAPI

Minha primeira tarefa foi criar uma API que seguisse os princípios RESTful. Optei pelo **FastAPI** por sua velocidade e por gerar a documentação interativa automaticamente, o que foi essencial para testar os endpoints. O arquivo `main.py` foi o centro de tudo, onde eu trabalhei com três exercícios progressivos para solidificar meu conhecimento.

* **HTTP Básico (Exercício 1):** Comecei com o básico, criando endpoints simples como o `/ping`, que serve para verificar se a API está online, e o `/echo`, que devolve uma saudação baseada no que recebe. Foi meu primeiro contato com os métodos `GET` e `POST` e com os `status codes` como `200 OK` e `201 Created`.
* **CRUD de Tarefas (Exercício 2):** Aqui, meu aprendizado aprofundou. Eu criei uma API completa de `CRUD` (Criar, Ler, Atualizar, Deletar) para um recurso de "tarefas". A API armazena os dados em memória, o que significa que as tarefas somem quando o servidor é reiniciado. Eu implementei os verbos HTTP correspondentes: `POST` para criar uma nova tarefa, `GET` para listar ou buscar uma tarefa por ID, `PUT` e `PATCH` para atualizações (completas e parciais, respectivamente) e `DELETE` para remover uma tarefa.
* **Autenticação e Rotas Protegidas (Exercício 3):** O desafio final foi adicionar uma camada de segurança. Eu criei uma rota de login que retorna um `token` de autenticação. Depois, usei uma `dependência` para proteger outras rotas, exigindo que o token fosse enviado no cabeçalho da requisição.

#### 2. Consumindo a API: O Frontend com Flask

Após construir o `backend`, meu próximo passo foi criar uma interface de usuário. Decidi usar o **Flask** por ser um `micro framework` simples e leve, perfeito para essa tarefa. O objetivo era que o `front-end` (o arquivo `client.py`) se comunicasse com a API que eu acabei de construir.

* Eu utilizei a biblioteca `requests` do Python para fazer todas as chamadas `HTTP` do `front-end` para o `back-end`. Cada ação do usuário no aplicativo `To-Do` (como adicionar, concluir ou excluir uma tarefa) se traduz em uma chamada `POST`, `PATCH` ou `DELETE` para a API.
* O uso de `render_template_string` no Flask me permitiu ter uma aplicação web funcional com todo o código em um único arquivo, focando na lógica de comunicação com a API. A interface é um aplicativo `To-Do` simples que mostra o status das tarefas como "Pendente" ou "Concluída".

#### 3. Testando e Validando a Solução

Uma parte crucial do processo foi garantir que a API e o `front-end` funcionavam como esperado. Eu utilizei duas ferramentas principais:

* **Documentação Interativa (Swagger UI):** A documentação gerada automaticamente pelo FastAPI na rota `/docs