# Sistema de Votação Online - MCP Redis

## 📋 Visão Geral

Esta é uma Single-Page Application (SPA) moderna para sistema de votação online que se conecta a um servidor MCP Redis local. A aplicação permite criar enquetes, votar em tempo real, e visualizar resultados com atualização automática via Pub/Sub.

## 🎯 Objetivo

Desenvolver uma aplicação web front-end moderna, intuitiva e responsiva para votação online, conectando-se a um servidor MCP Redis local (não público) rodando em Docker ou similar.

## 🚀 Funcionalidades Implementadas

### 1. **Conexão MCP Redis**
- Conexão WebSocket ao servidor MCP Redis local (configurável)
- Indicador visual de status (Conectando/Conectado/Erro)
- Reconexão automática em caso de falha

### 2. **Criação de Enquetes**
- Formulário modal com validação
- Campos: Título, múltiplas opções (mínimo 2), data/hora de expiração
- Comandos Redis utilizados:
  - `HSET` - Salvar dados da enquete como Hash
  - `ZADD` - Inicializar Sorted Set de votos
  - `SADD` - Adicionar à lista de enquetes ativas
  - `XADD` - Registrar evento de auditoria

### 3. **Sistema de Votação**
- Um voto por enquete por usuário (controle via localStorage)
- Comandos Redis utilizados:
  - `ZINCRBY` - Incrementar voto da opção no Sorted Set
  - `XADD` - Registrar voto no Stream de auditoria
  - `PUBLISH` - Notificar outros clientes da atualização

### 4. **Visualização e Rankings**
- Dashboard com lista de todas as enquetes ativas
- Visualização detalhada com gráficos de barras
- Resultados ordenados do mais votado para o menos votado
- Comandos Redis utilizados:
  - `SMEMBERS` - Listar enquetes ativas
  - `HGETALL` - Obter dados da enquete
  - `ZRANGE ... REV WITHSCORES` - Obter votos ordenados

### 5. **Atualização em Tempo Real (Pub/Sub)**
- Inscrição automática no canal `polls:updates`
- Atualização instantânea quando qualquer cliente vota
- Comandos Redis utilizados:
  - `SUBSCRIBE` - Inscrever no canal de atualizações
  - `PUBLISH` - Publicar atualização após voto

### 6. **Auditoria (Redis Streams)**
- Registro de todas as ações principais
- Stream: `audit:log`
- Eventos registrados: criação de enquete, votos
- Comando Redis utilizado:
  - `XADD` - Adicionar evento ao Stream

### 7. **Inteligência Artificial (MemoryForge)**
- Botão "Sugerir Título" no formulário de criação
- Consulta MemoryForge AI (se disponível no MCP)
- Fallback para sugestões predefinidas
- Baseado em títulos históricos do Stream de auditoria

## 🛠️ Tecnologias Utilizadas

- **HTML5** - Estrutura
- **Tailwind CSS** (CDN) - Estilização responsiva mobile-first
- **JavaScript (ES6+)** - Lógica da aplicação
- **WebSocket API** - Conexão com MCP Redis
- **Redis** - Banco de dados (via MCP)
  - Hash
  - Sorted Sets
  - Pub/Sub
  - Streams
  - Sets

## 🏗️ Arquitetura Técnica

### Duas Conexões WebSocket Separadas

A aplicação utiliza **DUAS conexões WebSocket independentes** para comunicação com o servidor MCP Redis:

#### 1️⃣ Conexão de Comandos (`mcpSocket`)
- **Propósito**: Executar comandos Redis regulares
- **Comandos suportados**: HSET, HGETALL, ZADD, ZINCRBY, ZRANGE, SADD, SMEMBERS, XADD, XRANGE, PUBLISH
- **Uso**: Criação de enquetes, votação, leitura de dados, auditoria

#### 2️⃣ Conexão Pub/Sub (`pubSubSocket`)
- **Propósito**: Exclusivo para subscrições Pub/Sub
- **Comandos suportados**: SUBSCRIBE
- **Uso**: Receber notificações em tempo real de atualizações de votos

### Por Que Duas Conexões?

No Redis, quando uma conexão entra em modo `SUBSCRIBE`, ela **só pode processar comandos de Pub/Sub** (SUBSCRIBE, UNSUBSCRIBE, PSUBSCRIBE, PUNSUBSCRIBE). Todos os outros comandos (HSET, ZADD, etc.) são bloqueados nessa conexão.

Portanto, para permitir que a aplicação:
- ✅ Crie enquetes e registre votos (comandos regulares)
- ✅ Receba atualizações em tempo real (Pub/Sub)

É **obrigatório** manter duas conexões WebSocket separadas.

### Reconexão Automática Robusta

Ambas as conexões implementam reconexão automática completa:

1. **Detecção de Falhas**: Tanto `onerror` quanto `onclose` disparam reconexão
2. **Rejeição de Promises**: Todas as requisições pendentes são rejeitadas para evitar travamentos
3. **Re-subscrição Automática**: O canal Pub/Sub é automaticamente re-inscrito após reconexão
4. **Handlers Completos**: Todos os event handlers são recriados em cada reconexão
5. **Backoff**: 5 segundos de intervalo entre tentativas de reconexão

### Fluxo de Dados

```
Criar Enquete:
  Cliente → mcpSocket → HSET → Redis
  Cliente → mcpSocket → ZADD → Redis
  Cliente → mcpSocket → SADD → Redis
  Cliente → mcpSocket → XADD → Redis (auditoria)

Votar:
  Cliente → mcpSocket → ZINCRBY → Redis (incrementar voto)
  Cliente → mcpSocket → PUBLISH → Redis (notificar outros)
  Cliente → mcpSocket → XADD → Redis (auditoria)
  
Receber Atualização em Tempo Real:
  Redis → pubSubSocket → Cliente (notificação via SUBSCRIBE)
  Cliente → mcpSocket → ZRANGE → Redis (recarregar dados)
```

## ⚙️ Configuração

### URL do Servidor MCP

No início do código JavaScript (linha ~160), há uma variável de configuração:

```javascript
const MCP_REDIS_URL = 'ws://localhost:3000';
```

**Ajuste esta URL** para corresponder ao endpoint do seu servidor MCP Redis local.

### Requisitos do Servidor MCP

O servidor MCP Redis deve suportar:
- Comandos Redis: HSET, HGETALL, ZADD, ZINCRBY, ZRANGE, SADD, SMEMBERS, XADD, XRANGE
- Pub/Sub: SUBSCRIBE, PUBLISH
- Protocolo WebSocket com formato JSON-RPC 2.0

## 📦 Estrutura de Dados Redis

### Enquetes (Hash)
```
poll:<uuid>
  - title: string
  - expiration: ISO 8601 datetime
  - options: JSON array
  - created: ISO 8601 datetime
```

### Votos (Sorted Set)
```
votes:<poll_id>
  - member: option_name
  - score: vote_count
```

### Enquetes Ativas (Set)
```
polls:active
  - members: poll:<uuid>, poll:<uuid>, ...
```

### Auditoria (Stream)
```
audit:log
  - entries: {action, timestamp, poll_id, option, title, ...}
```

### Canal Pub/Sub
```
polls:updates
  - messages: poll:<uuid>
```

## 🎨 Interface do Usuário

- **Design Responsivo** - Mobile-first com Tailwind CSS
- **Feedback Visual** - Mensagens claras de sucesso/erro
- **Indicador de Conexão** - Status em tempo real no header
- **Modais** - Criação de enquetes e visualização de detalhes
- **Gráficos de Barras** - Visualização de resultados com percentuais
- **Animações** - Transições suaves e pulse no indicador de conexão

## 📝 Como Usar

1. **Inicie seu servidor MCP Redis local** (ex: Docker em ws://localhost:3000)
2. **Abra o arquivo index.html** no navegador
3. **Aguarde a conexão** - O indicador deve ficar verde quando conectado
4. **Crie enquetes** - Clique em "Nova Enquete"
5. **Vote** - Clique em uma enquete e escolha sua opção
6. **Veja resultados em tempo real** - Atualizações automáticas via Pub/Sub

## 🔒 Segurança

- Escape de HTML para prevenir XSS
- Validação de formulários no cliente
- Controle de votação duplicada (localStorage)
- Data de expiração obrigatória no futuro

## 🐛 Debugging

Todas as interações com MCP são logadas no console do navegador:
- `📤 Enviado:` - Comandos enviados
- `📥 Recebido:` - Respostas recebidas
- `✅` - Operações bem-sucedidas
- `❌` - Erros

## 📄 Entregável

**Arquivo único:** `index.html`
- Todo o código HTML, CSS e JavaScript em um único arquivo
- Pronto para abrir diretamente no navegador
- Comentários extensivos em português
- Sem dependências externas (exceto Tailwind CDN)

## 🔄 Reconexão Automática

Se a conexão com o MCP cair, a aplicação tentará reconectar automaticamente a cada 5 segundos.

## 📊 Dados Persistentes

- Votos: Armazenados no Redis via MCP
- Controle de "já votou": localStorage do navegador
- Histórico: Redis Streams (auditoria completa)

## 🎯 Próximos Passos (Futuras Melhorias)

- Sistema de autenticação de usuários
- Edição e exclusão de enquetes
- Dashboard de analytics avançado
- Exportação de resultados (CSV/JSON)
- Limpeza automática de enquetes expiradas
- Temas escuro/claro
- Internacionalização (i18n)

## 📌 Notas Importantes

- A aplicação requer um servidor MCP Redis rodando localmente
- O Tailwind CSS é carregado via CDN (não use em produção final)
- O controle de votação é simples (localStorage) - para produção, implemente autenticação
- Todos os comandos Redis são executados via MCP (protocolo JSON-RPC 2.0)

---

**Data de Criação:** 25 de Outubro de 2025  
**Versão:** 1.0.0  
**Licença:** Open Source
