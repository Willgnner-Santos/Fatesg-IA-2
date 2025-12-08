# 🔗 Guia de Integração Frontend-Backend CogniKids

## 📋 Visão Geral

Este documento explica como o frontend Streamlit (CogniKids 3.0) se integra com o backend Flask (CogniKidsV2.0).

---

## 🏗️ Arquitetura da Integração

```
┌─────────────────────────────────────────┐
│   Frontend Streamlit (Porta 8501)      │
│   - Interface do usuário                │
│   - Visualizações e gráficos            │
│   - Lógica de apresentação              │
└──────────────┬──────────────────────────┘
               │ HTTP/REST
               │ (requests library)
               ▼
┌─────────────────────────────────────────┐
│   Backend Flask (Porta 5001)            │
│   - API REST                            │
│   - Autenticação JWT                    │
│   - Lógica de negócio                   │
│   - Acesso ao MongoDB                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   MongoDB (Porta 27017)                 │
│   - Armazenamento de dados              │
└─────────────────────────────────────────┘
```

---

## ⚙️ Configuração

### 1. Iniciar o Backend

Primeiro, certifique-se de que o backend está rodando:

```bash
# Navegue até a pasta do backend
cd "C:\Users\ACER\Desktop\GRADUAÇÃO I.A\2º Periodo\Pi\CogniKidsV2.0\cognikids-backend"

# Com Docker (recomendado)
docker-compose up

# Ou sem Docker
python run.py
```

O backend estará disponível em: **http://localhost:5001**

### 2. Verificar Conectividade

Teste se a API está respondendo:
```bash
curl http://localhost:5001/api/status
```

Ou acesse no navegador:
```
http://localhost:5001/docs
```

### 3. Iniciar o Frontend

```bash
# Navegue até a pasta do frontend
cd "C:\Users\ACER\Desktop\GRADUAÇÃO I.A\2º Periodo\Pi\CogniKids3.0\cognikids"

# Inicie o Streamlit
streamlit run app.py
```

O frontend estará disponível em: **http://localhost:8501**

---

## 🔐 Autenticação

### Sistema JWT

O backend usa **JSON Web Tokens (JWT)** para autenticação:

1. **Login**: Usuário envia credenciais → Backend retorna token
2. **Requisições**: Frontend inclui token no header `Authorization: Bearer <token>`
3. **Validação**: Backend valida token em cada requisição

### Fluxo de Login

```python
# 1. Usuário preenche formulário
email = "ana.sofia@aluno.dev"
password = "senha123"

# 2. Frontend faz requisição
response = api_client.login(email, password)

# 3. Backend valida e retorna
{
    "success": True,
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
        "user": {
            "_id": "507f1f77bcf86cd799439011",
            "nome": "Ana Sofia",
            "email": "ana.sofia@aluno.dev",
            "tipo": "aluno"
        }
    }
}

# 4. Frontend salva token na sessão
st.session_state['token'] = response['data']['token']
st.session_state['usuario_logado'] = response['data']['user']
```

---

## 📡 Endpoints Disponíveis

### Autenticação
- **POST** `/api/auth/register` - Registrar usuário
- **POST** `/api/auth/login` - Login

### Alunos
- **GET** `/api/students/{id}` - Perfil do aluno
- **GET** `/api/students/{id}/grades` - Notas do aluno
- **GET** `/api/students/{id}/challenges` - Desafios do aluno

### Atividades/Desafios
- **GET** `/api/challenges` - Listar desafios
- **POST** `/api/challenges/submit` - Enviar resposta

### Notas
- **POST** `/api/grades` - Salvar nota
- **GET** `/api/grades/student/{id}` - Notas do aluno

### IoT
- **GET** `/api/iot/student/{id}` - Dados biométricos
- **POST** `/api/iot/data` - Enviar dados de sensor

---

## 🛠️ Módulos de Integração

### `utils/api_client.py`

Cliente principal para comunicação com a API:

```python
from utils.api_client import api_client

# Login
result = api_client.login(email, password)

# Buscar notas
grades = api_client.get_student_grades(student_id)

# Salvar resposta
api_client.submit_challenge_response(
    challenge_id="123",
    student_id="456",
    answers=[...],
    score=85,
    time_spent=120.5
)
```

### `utils/helpers.py`

Funções auxiliares com fallback local:

```python
from utils.helpers import carregar_progresso, salvar_resposta

# Carrega dados (API primeiro, depois arquivo local)
df = carregar_progresso(usuario_id="123")

# Salva resposta (API primeiro, depois arquivo local)
salvar_resposta(
    usuario_id="123",
    tema="Matemática",
    acertos=8,
    total_questoes=10,
    tempo_resposta=45.2,
    pontuacao=80
)
```

---

## 🔄 Modo Híbrido (API + Local)

O sistema funciona em **modo híbrido**:

1. **API Disponível**: Usa endpoints do backend
2. **API Indisponível**: Usa arquivos JSON/CSV locais (fallback)

### Vantagens

- ✅ Funciona offline (desenvolvimento)
- ✅ Transição suave entre modos
- ✅ Melhor experiência do usuário
- ✅ Facilita testes

### Indicador de Status

No sidebar, há um indicador visual:
- 🟢 **API Conectada**: Usando backend
- 🟡 **Modo Offline**: Usando dados locais

---

## 👥 Contas de Teste

### Backend (banco MongoDB)

**Professores:**
- `carlos.antunes@escola.dev` / `senha123`
- `beatriz.moreira@escola.dev` / `senha123`

**Pais/Responsáveis:**
- `ricardo.alves@pais.dev` / `senha123`
- `mariana.costa@pais.dev` / `senha123`
- `helena.mendes@pais.dev` / `senha123`

**Alunos:**
- `ana.sofia@aluno.dev` / `senha123`
- `bruno.costa@aluno.dev` / `senha123`
- `clara.lima@aluno.dev` / `senha123`
- `diogo.mendes@aluno.dev` / `senha123`

### Local (fallback)
- `maria` / `123`
- `joao` / `456`
- `ana` / `789`

---

## 🐛 Troubleshooting

### Erro: "Não foi possível conectar ao servidor"

**Causa**: Backend não está rodando

**Solução**:
```bash
cd cognikids-backend
docker-compose up
# ou
python run.py
```

### Erro: "401 Unauthorized"

**Causa**: Token expirado ou inválido

**Solução**: Faça logout e login novamente

### Backend respondendo mas dados não aparecem

**Causa**: Dados não foram populados no MongoDB

**Solução**:
```bash
cd cognikids-backend
python scripts/populate_mongo.py
```

### Porta 5001 já está em uso

**Solução**:
```bash
# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# Ou altere a porta em .env do backend
```

---

## 📊 Fluxo de Dados

### Exemplo: Completar uma atividade

```
1. Aluno responde questões no frontend
   ↓
2. Frontend calcula pontuação e tempo
   ↓
3. Frontend chama api_client.submit_challenge_response()
   ↓
4. API Client envia POST para /api/challenges/submit
   ↓
5. Backend valida token JWT
   ↓
6. Backend salva no MongoDB
   ↓
7. Backend retorna confirmação
   ↓
8. Frontend atualiza interface
   ↓
9. Frontend mostra feedback visual
```

---

## 🚀 Próximos Passos

- [ ] Implementar cache de requisições
- [ ] Adicionar retry automático em falhas
- [ ] Implementar sincronização offline
- [ ] Adicionar mais endpoints (fórum, mensagens, etc)
- [ ] Melhorar tratamento de erros
- [ ] Adicionar testes de integração

---

## 📚 Referências

- **Backend**: `C:\Users\ACER\Desktop\GRADUAÇÃO I.A\2º Periodo\Pi\CogniKidsV2.0\cognikids-backend`
- **Frontend**: `C:\Users\ACER\Desktop\GRADUAÇÃO I.A\2º Periodo\Pi\CogniKids3.0\cognikids`
- **Documentação API**: http://localhost:5001/docs
- **Swagger JSON**: `cognikids-backend/swagger.json`

---

**Desenvolvido com ❤️ para o projeto CogniKids**
