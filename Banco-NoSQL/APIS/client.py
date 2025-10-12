# -------------------------------------------------------------------------
# Importações de bibliotecas
# -------------------------------------------------------------------------

from flask import Flask, render_template_string, request, redirect, url_for
# Flask → micro framework web em Python, usado aqui para criar o "front"
# render_template_string → permite escrever HTML diretamente dentro do Python
# request → objeto que captura informações da requisição do usuário (ex.: formulários)
# redirect → envia o navegador para outra página/rota automaticamente
# url_for → gera a URL de uma rota Flask pelo nome da função (ex.: url_for("index") → "/")

import requests
# requests → biblioteca em Python para fazer chamadas HTTP (GET, POST, PATCH, DELETE)
# Vamos usá-la para o Flask conversar com a API FastAPI

# -------------------------------------------------------------------------
# Configuração inicial
# -------------------------------------------------------------------------

API_URL = "http://127.0.0.1:8000/api/v1"
# Endereço base da nossa API FastAPI.
# Ou seja, sempre que chamarmos GET, POST, PATCH, DELETE,
# vamos montar a URL começando com esse prefixo.

app = Flask(__name__)
# Cria a aplicação Flask. A variável "app" representa nosso servidor.

# -------------------------------------------------------------------------
# HTML (interface do usuário)
# -------------------------------------------------------------------------
# Este é o código HTML que será renderizado no navegador.
# Ele define:
# - Um formulário para adicionar nova tarefa
# - Uma tabela para listar, concluir/reabrir e excluir tarefas
# - Usa o Bootstrap (biblioteca de CSS) para deixar a página bonita

TEMPLATE = """
<!doctype html>
<html lang="pt-br">
  <head>
    <meta charset="utf-8">
    <title>To-Do App (Flask + FastAPI)</title>
    <!-- Bootstrap (CSS pronto para deixar a tabela e botões bonitos) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <div class="container py-4">
      <h1 class="mb-4">✅ Mini To-Do App</h1>

      <!-- Formulário para criar nova tarefa -->
      <form action="{{ url_for('add_task') }}" method="post" class="row g-2 mb-4">
        <div class="col-auto">
          <!-- Campo de entrada de texto (name="titulo") → será enviado no POST -->
          <input type="text" class="form-control" name="titulo" placeholder="Nova tarefa" required>
        </div>
        <div class="col-auto">
          <button type="submit" class="btn btn-success">Adicionar</button>
        </div>
      </form>

      <!-- Tabela mostrando todas as tarefas -->
      <table class="table table-striped table-bordered">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <!-- Loop em todas as tarefas recebidas do back -->
          {% for task in tasks %}
          <tr>
            <!-- task.id → mostra o ID da tarefa -->
            <td>{{ task.id }}</td>
            <!-- task.title → mostra o título -->
            <td>{{ task.title }}</td>
            <!-- task.done → campo booleano (True/False) que indica se está concluída -->
            <td>
              {% if task.done %}
                <!-- Se done=True → concluída -->
                <span class="badge bg-success">Concluída</span>
              {% else %}
                <!-- Se done=False → pendente -->
                <span class="badge bg-warning text-dark">Pendente</span>
              {% endif %}
            </td>
            <td>
              <!-- Botão que chama rota toggle_task para inverter o status -->
              <a href="{{ url_for('toggle_task', task_id=task.id) }}" class="btn btn-sm btn-info">
                {% if task.done %} Reabrir {% else %} Concluir {% endif %}
              </a>
              <!-- Botão que chama rota delete_task para excluir -->
              <a href="{{ url_for('delete_task', task_id=task.id) }}" class="btn btn-sm btn-danger">Excluir</a>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </body>
</html>
"""

# -------------------------------------------------------------------------
# Rotas do Flask (cada uma representa uma ação no front)
# -------------------------------------------------------------------------

@app.route("/")  # Define que essa função responde ao endereço "/"
def index():
    """
    Página inicial.
    - Faz um GET no back-end (FastAPI → /tasks).
    - Recebe a lista de tarefas em JSON.
    - Renderiza o HTML (TEMPLATE) passando a lista de tasks.
    """
    resp = requests.get(f"{API_URL}/tasks")  # GET → busca lista de tarefas
    tasks = resp.json()  # Converte a resposta JSON em lista/dicionário Python
    return render_template_string(TEMPLATE, tasks=tasks)
    # Renderiza o HTML, preenchendo "{{ tasks }}" com a lista recebida


@app.route("/add", methods=["POST"])  # Essa rota só aceita POST
def add_task():
    """
    Adiciona uma nova tarefa.
    - Captura o campo "titulo" enviado pelo formulário.
    - Cria um dicionário com {"title": titulo}.
    - Envia esse dicionário como JSON no POST para a API FastAPI (/tasks).
    - Redireciona para "/" para atualizar a lista.
    """
    titulo = request.form["titulo"]  
    # request.form → contém os dados enviados pelo formulário HTML.
    # Aqui pegamos o valor do campo name="titulo".

    payload = {"title": titulo}  
    # payload → "carga útil" que será enviada para a API.
    # É um dicionário Python com chave "title" e valor o título digitado.
    # Exemplo: {"title": "Estudar Python"}

    requests.post(f"{API_URL}/tasks", json=payload)  
    # Faz a chamada POST para a API.
    # O parâmetro json= converte automaticamente o dicionário em JSON.

    return redirect(url_for("index"))  
    # Após adicionar, redireciona para a rota "index" ("/").
    # Isso atualiza a tabela de tarefas.


@app.route("/delete/<int:task_id>")  # Define rota dinâmica, recebe um número (int) na URL
def delete_task(task_id):
    """
    Exclui uma tarefa.
    - task_id é capturado da URL (ex.: /delete/3 → task_id=3).
    - Faz um DELETE na API FastAPI (/tasks/{id}).
    - Depois volta para "/" para recarregar a tabela.
    """
    requests.delete(f"{API_URL}/tasks/{task_id}")
    # Monta a URL com f-string (ex.: /tasks/3).
    # DELETE remove essa tarefa no back-end.

    return redirect(url_for("index"))
    # Redireciona para "/" (rota index) para atualizar a tabela.


@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    """
    Alterna o status de uma tarefa (pendente <-> concluída).
    - Busca a tarefa atual no back (GET /tasks/{id}).
    - Lê o valor atual de "done".
    - Cria um payload invertendo esse valor.
    - Faz PATCH na API para atualizar apenas o campo "done".
    - Redireciona para "/" para atualizar a tabela.
    """
    task = requests.get(f"{API_URL}/tasks/{task_id}").json()
    # Busca os dados da tarefa pelo ID.
    # A resposta é um dicionário, ex. {"id": 1, "title": "Estudar", "done": False}

    new_done = not task["done"]
    # task["done"] → acessa o valor do campo "done" (booleano).
    # not inverte o valor (True → False, False → True).
    # new_done será o novo estado que queremos aplicar.

    payload = {"done": new_done}
    # payload é um dicionário que envia a atualização para o back-end.
    # A chave "done" é o nome do campo na API.
    # O ":" separa a chave do valor → {"chave": valor}.
    # Aqui: chave "done", valor new_done (True ou False).

    requests.patch(f"{API_URL}/tasks/{task_id}", json=payload)
    # PATCH → atualização parcial.
    # Envia apenas {"done": True/False} sem precisar mandar o objeto inteiro.

    return redirect(url_for("index"))
    # Redireciona para "/" para mostrar a tabela atualizada.


# -------------------------------------------------------------------------
# Execução do servidor Flask
# -------------------------------------------------------------------------
if __name__ == "__main__":  
    # Esse if garante que o app só roda se chamarmos esse arquivo diretamente
    # (não roda se ele for importado em outro script).
    
    app.run(debug=True)  
    # Inicia o servidor Flask em http://127.0.0.1:5000
    # debug=True → recarrega automaticamente em caso de alterações.
