"""
main_comentado.py — API de exemplo com FastAPI
-----------------------------------------------
Este arquivo contém 3 exercícios progressivos para iniciantes em APIs:

Exercício 1: HTTP básico (GET/POST) e Status Codes
Exercício 2: CRUD RESTful do recurso 'tasks' (em memória)
Exercício 3: Autenticação simples (login) + middleware por dependência + CORS

Observação:
- Os dados de 'tasks' ficam em memória → somem quando o servidor reinicia.
- O código foi **comentado linha por linha** para facilitar o estudo.
"""  # Docstring de topo: descreve o arquivo e os exercícios

# ------------------------------------------------------------------------------  # Separador visual para organização do código
# Importações necessárias
# ------------------------------------------------------------------------------  # Fim do bloco de título

from typing import List, Optional   # Tipos para anotações (listas e valores opcionais)
from fastapi import (               # Importa FastAPI e utilitários do framework
    FastAPI,                        # Classe principal para criar a aplicação
    HTTPException,                  # Exceção HTTP para retornar erros padronizados
    status,                         # Enum com códigos HTTP (200, 404, 201 etc.)
    Response,                       # Objeto de resposta, permite ajustar headers e status
    Header,                         # Lê valores do cabeçalho da requisição
    Depends,                        # Injeta dependências (ex.: middleware por função)
)  # Fecha o bloco de import do fastapi
from fastapi.middleware.cors import CORSMiddleware  # Middleware para habilitar CORS
from pydantic import BaseModel, Field               # Pydantic para validação de dados

# ------------------------------------------------------------------------------  # Separador visual
# Configuração inicial da aplicação
# ------------------------------------------------------------------------------  # Fim do título

# Criamos a aplicação FastAPI
app = FastAPI(  # Instancia o app FastAPI
    title="Aula de APIs com FastAPI",       # Nome exibido na documentação (/docs)
    description=(  # Descrição da API exibida no Swagger/Redoc
        "API didática para iniciantes: GET/POST, CRUD RESTful e autenticação simples.\n\n"
        "Use a aba **/docs** (Swagger) para testar os endpoints diretamente no navegador."
    ),  # Fim da descrição
    version="1.0.0",                        # Versão da API
    openapi_tags=[                            # Lista de tags para agrupar endpoints
        {"name": "Exercício 1 — HTTP básico", "description": "Endpoints simples de GET e POST com status code."},  # Tag do exercício 1
        {"name": "Exercício 2 — Tasks (CRUD RESTful)", "description": "CRUD do recurso `/api/v1/tasks` em memória."},  # Tag do exercício 2
        {"name": "Exercício 3 — Auth + rotas protegidas", "description": "Login que retorna token e rotas protegidas por header Authorization."},  # Tag do exercício 3
        {"name": "Utilidades", "description": "Rotas de utilidade geral."},  # Tag de utilidades
    ],  # Fim da lista de tags
)  # Fecha a criação do app

# ------------------------------------------------------------------------------  # Separador
# Middleware de CORS (Cross-Origin Resource Sharing)
# Permite que front-ends em outros domínios consumam a API
# ------------------------------------------------------------------------------  # Fim do título

app.add_middleware(  # Registra o middleware de CORS no app
    CORSMiddleware,  # Classe do middleware
    allow_origins=["*"],     # "*" permite qualquer origem (em produção, restrinja a domínios confiáveis)
    allow_credentials=False, # Desabilita envio automático de cookies/credenciais
    allow_methods=["*"],     # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Permite qualquer cabeçalho na requisição
)  # Fecha a configuração do CORS

# ------------------------------------------------------------------------------  # Separador
# Modelos (Schemas) com Pydantic
# ------------------------------------------------------------------------------  # Fim do título

# ==== Exercício 1 ====  # Início dos modelos do exercício 1
class EchoIn(BaseModel):  # Modelo de entrada para o POST /api/v1/echo
    """Modelo do corpo esperado pelo POST /api/v1/echo"""  # Docstring explicativa
    name: str = Field(..., min_length=1, description="Nome da pessoa para saudação.")  # Campo obrigatório 'name'

class EchoOut(BaseModel):  # Modelo de saída para o POST /api/v1/echo
    """Modelo de resposta do POST /api/v1/echo"""  # Docstring explicativa
    hello: str = Field(..., description="Mensagem de saudação personalizada.")  # Campo 'hello' retornado


# ==== Exercício 2 (Tasks) ====  # Início dos modelos para tarefas
class Task(BaseModel):  # Representação completa de uma tarefa (saída da API)
    """Representação completa de uma tarefa (retorno da API)."""  # Docstring
    id: int  # Identificador único da tarefa
    title: str = Field(..., min_length=1, description="Título da tarefa.")  # Título da tarefa (obrigatório)
    done: bool = Field(default=False, description="Marcação de conclusão da tarefa.")  # Status de conclusão

class TaskCreate(BaseModel):  # Modelo usado para criar uma nova tarefa
    """Modelo usado para criar uma nova tarefa (entrada do POST)."""  # Docstring
    title: str = Field(..., min_length=1, description="Título da nova tarefa.")  # Apenas o título é necessário

class TaskPut(BaseModel):  # Modelo para atualização completa (PUT)
    """Modelo de atualização completa (PUT) → precisa de todos os campos."""  # Docstring
    title: str = Field(..., min_length=1)  # Título obrigatório
    done: bool  # Flag done obrigatória

class TaskPatch(BaseModel):  # Modelo para atualização parcial (PATCH)
    """Modelo de atualização parcial (PATCH) → pode enviar só o que quer mudar."""  # Docstring
    title: Optional[str] = Field(default=None, min_length=1)  # Título opcional
    done: Optional[bool] = None  # Flag done opcional


# ==== Exercício 3 (Auth) ====  # Início dos modelos de autenticação
class LoginIn(BaseModel):  # Modelo de credenciais de entrada
    """Credenciais de login (entrada)."""  # Docstring
    username: str  # Nome de usuário
    password: str  # Senha

class LoginOut(BaseModel):  # Modelo de retorno do login
    """Modelo de saída do login (token fake)."""  # Docstring
    token: str  # Token retornado ao efetuar login


# ------------------------------------------------------------------------------  # Separador
# "Banco de dados" em memória (apenas para fins didáticos)
# ------------------------------------------------------------------------------  # Fim do título

tasks_db: List[Task] = [Task(id=1, title="Estudar APIs", done=False)]  # Lista de tarefas em memória (começa com 1 tarefa)
_next_id = 2  # Contador para IDs incrementais (simula autoincremento de banco)

# ------------------------------------------------------------------------------  # Separador
# Exercício 1 — HTTP básico
# ------------------------------------------------------------------------------  # Fim do título

@app.get("/api/v1/ping", response_model=dict, tags=["Exercício 1 — HTTP básico"])  # Define rota GET /api/v1/ping
def ping():  # Função que atende a rota /api/v1/ping
    """
    Teste rápido de disponibilidade (health-check).
    Retorna {"ok": true, "message": "pong"} com status 200.
    """  # Docstring da função explicando o retorno
    return {"ok": True, "message": "pong"}  # Retorna um dicionário simples confirmando que a API está viva


@app.post(  # Define rota POST para /api/v1/echo
    "/api/v1/echo",                    # Caminho da rota
    response_model=EchoOut,            # Modelo de resposta → garante consistência no retorno
    status_code=status.HTTP_201_CREATED, # Retornará HTTP 201 Created
    tags=["Exercício 1 — HTTP básico"], # Tag para agrupar no Swagger
)  # Fim do decorador .post
def echo(payload: EchoIn):             # Função que recebe o corpo validado por EchoIn
    """
    Recebe um JSON com o campo 'name' e devolve uma saudação.
    """  # Docstring com a descrição do que a rota faz
    return EchoOut(hello=f"Olá, {payload.name}!")  # Cria resposta no formato EchoOut com saudação personalizada


# ------------------------------------------------------------------------------  # Separador
# Exercício 2 — CRUD RESTful (Tasks)
# ------------------------------------------------------------------------------  # Fim do título

@app.get("/api/v1/tasks", response_model=List[Task], tags=["Exercício 2 — Tasks (CRUD RESTful)"])  # Lista todas as tarefas
def list_tasks():  # Função para listar tarefas
    """Lista todas as tarefas armazenadas em memória."""  # Docstring resumindo a operação
    return tasks_db  # Retorna a lista de tarefas inteira


@app.get("/api/v1/tasks/{task_id}", response_model=Task, tags=["Exercício 2 — Tasks (CRUD RESTful)"])  # Busca tarefa por ID
def get_task(task_id: int):  # Recebe o ID como parâmetro de rota e tipa como int
    """Busca uma tarefa pelo ID. Retorna 404 se não existir."""  # Docstring da função
    for task in tasks_db:  # Percorre a lista de tarefas
        if task.id == task_id:  # Verifica se a tarefa atual tem o ID procurado
            return task  # Retorna a tarefa encontrada
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")  # Se não achar, levanta 404


@app.post(  # Define rota POST para criar tarefa
    "/api/v1/tasks",  # Caminho da rota
    response_model=Task,  # Modelo de saída será Task completa
    status_code=status.HTTP_201_CREATED,  # Retorna 201 se criada
    tags=["Exercício 2 — Tasks (CRUD RESTful)"],  # Tag no Swagger
)  # Fim do decorador .post
def create_task(payload: TaskCreate, response: Response):  # Função que recebe payload validado e objeto Response
    """Cria uma nova tarefa."""  # Docstring
    global _next_id  # Usa o contador global para gerar o próximo ID
    task = Task(id=_next_id, title=payload.title, done=False)  # Instancia a nova Task com done=False por padrão
    tasks_db.append(task)                                     # Adiciona a tarefa criada ao "banco" em memória
    _next_id += 1                                            # Incrementa o contador para o próximo uso
    response.headers["Location"] = f"/api/v1/tasks/{task.id}" # Boa prática REST: indica a URL do novo recurso
    return task                                              # Retorna a tarefa criada (aparece no corpo da resposta)


@app.put("/api/v1/tasks/{task_id}", response_model=Task, tags=["Exercício 2 — Tasks (CRUD RESTful)"])  # Atualiza COMPLETAMENTE uma tarefa
def put_task(task_id: int, payload: TaskPut):  # Recebe ID e corpo com todos os campos obrigatórios
    """Atualiza COMPLETAMENTE uma tarefa existente (PUT)."""  # Docstring
    for i, t in enumerate(tasks_db):  # Percorre a lista com índice para poder substituir
        if t.id == task_id:  # Se encontrou a tarefa pelo ID
            updated = Task(id=task_id, title=payload.title, done=payload.done)  # Cria novo objeto Task com dados atualizados
            tasks_db[i] = updated  # Substitui a posição i pela nova tarefa
            return updated  # Retorna a tarefa atualizada
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")  # Se não achar, retorna 404


@app.patch("/api/v1/tasks/{task_id}", response_model=Task, tags=["Exercício 2 — Tasks (CRUD RESTful)"])  # Atualiza PARCIALMENTE
def patch_task(task_id: int, payload: TaskPatch):  # Recebe ID e campos opcionais para atualização
    """Atualiza PARCIALMENTE uma tarefa (PATCH)."""  # Docstring
    for i, t in enumerate(tasks_db):  # Percorre a lista com índice
        if t.id == task_id:  # Encontrou a tarefa
            # Atualiza apenas os campos enviados  # Comentário explicativo
            new_title = t.title if payload.title is None else payload.title  # Mantém título antigo se não enviado
            new_done = t.done if payload.done is None else payload.done      # Mantém done antigo se não enviado
            updated = Task(id=task_id, title=new_title, done=new_done)       # Cria nova Task com as mudanças
            tasks_db[i] = updated  # Substitui na lista
            return updated  # Retorna a tarefa parcialmente atualizada
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")  # 404 se não existir


@app.delete("/api/v1/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Exercício 2 — Tasks (CRUD RESTful)"])  # Deleta tarefa
def delete_task(task_id: int):  # Recebe o ID da tarefa a deletar
    """Deleta uma tarefa. Retorna 204 (No Content)."""  # Docstring
    global tasks_db  # Indica que vamos reatribuir a variável global tasks_db
    before = len(tasks_db)  # Guarda o tamanho da lista antes da remoção
    tasks_db = [t for t in tasks_db if t.id != task_id]  # Cria nova lista sem a tarefa do ID informado
    if len(tasks_db) == before:  # Se o tamanho não mudou, nenhuma tarefa foi removida
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada")  # Retorna 404
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Devolve 204 (sem corpo na resposta)


# ------------------------------------------------------------------------------  # Separador
# Exercício 3 — Autenticação simples (token fixo)
# ------------------------------------------------------------------------------  # Fim do título

FAKE_TOKEN = "aluno123"  # Token fixo usado apenas para fins didáticos (NÃO usar em produção)


def require_token(authorization: Optional[str] = Header(default=None)):  # Dependência que valida o header Authorization
    """Middleware por dependência que exige um token no cabeçalho Authorization."""  # Docstring
    if not authorization:  # Se o cabeçalho não foi enviado
        raise HTTPException(  # Retorna 401 (sem credenciais)
            status_code=status.HTTP_401_UNAUTHORIZED,  # Código 401
            detail="Missing Authorization header",  # Mensagem de erro
            headers={"WWW-Authenticate": "Bearer"},  # Indica o esquema esperado
        )  # Fim da exceção
    try:  # Tenta separar o esquema e o token
        scheme, token = authorization.split(" ")  # Espera formato "Bearer <token>"
    except ValueError:  # Se não houver espaço para split (formato errado)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization format")  # 401

    if scheme != "Bearer":  # Verifica se o esquema é Bearer
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization scheme must be Bearer")  # 401

    if token != FAKE_TOKEN:  # Compara o token recebido com o token esperado
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")  # 403 se token inválido


@app.post("/api/v1/auth/login", response_model=LoginOut, tags=["Exercício 3 — Auth + rotas protegidas"])  # Endpoint de login
def login(creds: LoginIn):  # Recebe credenciais validadas pelo modelo LoginIn
    """Faz login e retorna o token fake se usuário=aluno e senha=1234."""  # Docstring
    if creds.username == "aluno" and creds.password == "1234":  # Verifica credenciais simples
        return LoginOut(token=FAKE_TOKEN)  # Retorna o token fake encapsulado no modelo LoginOut
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")  # Caso contrário, 401


@app.get("/api/v1/secure/tasks", response_model=List[Task], tags=["Exercício 3 — Auth + rotas protegidas"])  # Lista tarefas protegidas
def secure_list_tasks(_=Depends(require_token)):  # Depende de require_token para autorizar
    """Lista tarefas em rota protegida por token."""  # Docstring
    return tasks_db  # Retorna as tarefas se o token for válido


@app.post(  # Rota POST protegida para criar tarefa
    "/api/v1/secure/tasks",  # Caminho da rota
    response_model=Task,  # Resposta será o objeto Task criado
    status_code=status.HTTP_201_CREATED,  # 201 Created
    tags=["Exercício 3 — Auth + rotas protegidas"],  # Tag no Swagger
)  # Fim do decorador .post
def secure_create_task(payload: TaskCreate, response: Response, _=Depends(require_token)):  # Requer token via Depends
    """Cria tarefa em rota protegida (precisa enviar Authorization: Bearer aluno123)."""  # Docstring
    global _next_id  # Usa o contador global para ID
    task = Task(id=_next_id, title=payload.title, done=False)  # Cria a nova tarefa com título do payload
    tasks_db.append(task)  # Adiciona ao "banco" em memória
    _next_id += 1  # Incrementa o contador de IDs
    response.headers["Location"] = f"/api/v1/secure/tasks/{task.id}"  # Informa a URL do novo recurso protegido
    return task  # Retorna a tarefa criada


# ------------------------------------------------------------------------------  # Separador
# Utilidades e rota raiz
# ------------------------------------------------------------------------------  # Fim do título

@app.get("/", tags=["Utilidades"])  # Define a rota raiz (home) da API
def root():  # Função que atende a rota "/"
    """Rota inicial com links úteis."""  # Docstring
    return {  # Retorna um dicionário com informações úteis
        "message": "Bem-vindo à API de exemplo!",  # Mensagem de boas-vindas
        "docs": "/docs",  # Link para documentação Swagger
        "redoc": "/redoc",  # Link para documentação ReDoc
        "exemplos": {  # Sub-seção com exemplos de rotas
            "ping": "/api/v1/ping",  # Exemplo de health-check
            "echo": "/api/v1/echo",  # Exemplo de POST com corpo
            "tasks": "/api/v1/tasks",  # CRUD público de tarefas
            "login": "/api/v1/auth/login",  # Rota de login
            "tasks_protegidas": "/api/v1/secure/tasks",  # Lista tarefas protegidas (requer token)
        },  # Fim da chave "exemplos"
    }  # Fim do dicionário de retorno
