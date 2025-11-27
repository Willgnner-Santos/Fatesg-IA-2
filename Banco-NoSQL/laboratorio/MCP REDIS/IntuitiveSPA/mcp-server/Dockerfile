FROM node:18-alpine

WORKDIR /app

# Instalar dependências
RUN npm init -y && \
    npm install ws redis express

# Copiar servidor
COPY server.js .

EXPOSE 3000

CMD ["node", "server.js"]