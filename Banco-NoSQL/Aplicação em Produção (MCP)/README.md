# Smart Presence Register 🚀

Sistema de Registro de Presença Inteligente desenvolvido em Node.js com Express, Redis e React.

<!--
  Este projeto foi desenvolvido utilizando uma arquitetura que previa a integração com uma API de Model Context Protocol (MCP) Redis fornecida pelo professor. No entanto, a API do MCP Redis não está mais disponível. Por isso, o projeto foi adaptado para funcionar de forma local, usando mpc redis e o redis localmente.
-->

## 🏗️ Arquitetura

- **Backend**: Node.js + Express + TypeScript
- **Frontend**: React + TypeScript + Vite + TailwindCSS
- **Banco de Dados**: Redis (Sorted Sets para ordenação automática)
- **MCP Server**: Model Context Protocol para integração com LLMs
- **Containerização**: Docker + Docker Compose

## 📋 Pré-requisitos

- Node.js 18+ 
- Docker Desktop
- PowerShell (Windows)

## 🚀 Como Executar Localmente

### 1. Clone e Configure o Projeto

```powershell
# Navegue até o diretório do projeto
cd "c:\Users\ACER\Desktop\GRADUAÇÃO I.A\2º Periodo\NoSql\Atividades\N2\MCP REDIS\SmartPresenceRegister"

# Instale as dependências
npm install
```

### 2. Inicie o Redis com Docker

```powershell
# Suba o container do Redis e MCP Server
docker-compose up -d

# Verifique se está rodando
docker-compose ps
```

### 3. Teste o MCP Redis Server

```powershell
# Execute o teste do MCP Redis
node test-mcp-redis.js
```

### 3. Execute a Aplicação

```powershell
# Desenvolvimento (com hot reload)
npm run dev

# OU execute tudo de uma vez
npm run setup
```

### 4. Acesse a Aplicação

- **Frontend**: http://localhost:5000
- **API**: http://localhost:5000/api
- **Redis Commander** (interface visual): http://localhost:8081
- **MCP Redis Server**: Disponível via stdio (integração com LLMs)

## 🔧 Scripts Disponíveis

```powershell
# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Executar build
npm run start

# Gerenciar Docker
npm run docker:up      # Sobe o Redis
npm run docker:down    # Para o Redis
npm run docker:logs    # Visualiza logs do Redis

# Setup completo
npm run setup          # Instala deps + sobe Redis + inicia dev
```

## 🤖 Servidor MCP Redis

O projeto inclui um servidor **Model Context Protocol (MCP)** que permite integração direta com LLMs (Large Language Models) para manipular dados do Redis.

### Ferramentas MCP Disponíveis:

- `redis_set` - Define valor para uma chave
- `redis_get` - Obtém valor de uma chave  
- `redis_del` - Deleta uma chave
- `redis_keys` - Lista chaves por padrão
- `redis_zadd` - Adiciona elemento a um Sorted Set
- `redis_zrange` - Obtém elementos de um Sorted Set
- `redis_hset` - Define campo em um Hash
- `redis_hget` - Obtém campo de um Hash
- `redis_info` - Informações do servidor Redis

### Como usar o MCP:

1. **Via VS Code**: Configure o `mcp-config.json`
2. **Via linha de comando**: Execute o servidor MCP diretamente
3. **Via Docker**: O servidor MCP está incluído no docker-compose

```powershell
# Executar apenas o servidor MCP
cd mcp-server
npm install
npm run build
npm start
```

## 🗃️ Estrutura do Banco (Redis)

O sistema usa **Redis Sorted Sets** para armazenar as presenças:

- **Key**: `presencas`
- **Score**: timestamp (garante ordenação automática)
- **Value**: JSON com dados da presença

### Exemplo de dados:
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "curso": "Ciência da Computação",
  "horario": "2024-10-25T10:30:00.000Z",
  "timestamp": 1729854600000
}
```

## 🐳 Docker Commands

```powershell
# Verificar status
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f redis

# Parar containers
docker-compose down

# Limpar volumes (remove dados)
docker-compose down -v
```

## 🔍 Monitoramento

### Redis Commander
Acesse http://localhost:8081 para visualizar:
- Dados armazenados
- Estatísticas do Redis
- Monitoramento em tempo real

### Logs da Aplicação
```powershell
# Durante desenvolvimento
npm run dev

# Logs do Redis
npm run docker:logs
```

## 🌐 Endpoints da API

### Registrar Presença
```http
POST /api/presenca
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@email.com",
  "curso": "Ciência da Computação"
}
```

### Obter Ranking
```http
GET /api/ranking
```

## 🛠️ Troubleshooting

### Redis não conecta
```powershell
# Verifique se o Docker está rodando
docker --version

# Verifique se o Redis está ativo
docker-compose ps

# Reinicie o Redis
docker-compose restart redis
```

### Erro de porta ocupada
```powershell
# Encontre processo usando a porta 5000
netstat -ano | findstr :5000

# Mate o processo (substitua PID)
taskkill /PID <PID> /F
```

### Limpar cache/dados
```powershell
# Remove containers e volumes
docker-compose down -v

# Remove node_modules
Remove-Item -Recurse -Force node_modules

# Reinstala dependências
npm install
```

## 📱 Funcionalidades

- ✅ Registro de presença com timestamp automático
- ✅ Ranking ordenado por ordem de chegada
- ✅ Interface responsiva (mobile-first)
- ✅ Validação de dados (Zod)
- ✅ Persistência em Redis
- ✅ Hot reload em desenvolvimento
- ✅ Logs estruturados
- ✅ Interface visual do Redis

## 🚀 Deploy em Produção

Para deploy em produção, configure:

1. **REDIS_URL** com Redis em nuvem (Upstash, Redis Cloud)
2. **NODE_ENV=production**
3. **PORT** conforme necessário

```bash
npm run build
npm start
```

---

**Desenvolvido com  Node.js, Redis e React**