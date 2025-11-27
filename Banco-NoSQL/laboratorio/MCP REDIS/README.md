# MCP REDIS - IntuitiveSPA

Este repositório contém o projeto IntuitiveSPA, uma Single Page Application (SPA) com um backend Node.js que utiliza Redis.

## Visão Geral

O projeto consiste em uma aplicação web front-end moderna e intuitiva, desenvolvida como uma SPA. O backend é construído com Node.js e se integra com o Redis para gerenciamento de dados e comunicação em tempo real, usando WebSockets.

## Estrutura do Projeto

A estrutura de pastas do projeto é a seguinte:

- **Evidencia 01.png, Evidencia 02.png, Evidencia 03.png, Evidencia 04.png**: Imagens de evidência do projeto.
- **IntuitiveSPA/**: Diretório principal da aplicação.
  - **.gitignore**: Arquivo para ignorar arquivos no Git.
  - **docker-compose-full.yml, docker-compose.yml**: Arquivos de configuração do Docker Compose para orquestração de contêineres.
  - **index.html**: Arquivo principal da SPA.
  - **server.ps1, simple-server.js, simple-server.ps1**: Scripts para iniciar servidores de desenvolvimento.
  - **test-websocket.html**: Página de teste para a comunicação via WebSocket.
  - **mcp-server/**: Contém o código do servidor backend.
    - **Dockerfile**: Arquivo para construir a imagem Docker do servidor.
    - **server.js**: Código-fonte do servidor Node.js.
    - **node_modules/**: Diretório de módulos do Node.js.

## Como Começar

Para executar este projeto, você precisará ter o Docker e o Docker Compose instalados.

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   ```
2. Navegue até o diretório `IntuitiveSPA`:
   ```bash
   cd "IntuitiveSPA"
   ```
3. Inicie os contêineres Docker:
   ```bash
   docker-compose up -d
   ```

A aplicação estará acessível em `http://localhost:8080` (ou a porta configurada no `docker-compose.yml`).


