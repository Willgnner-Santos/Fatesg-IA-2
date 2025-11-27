// Usar require
const WebSocket = require('ws');
const redis = require('redis');
const express = require('express');

const app = express();
const server = require('http').createServer(app);

// Configurar Redis
const REDIS_HOST = process.env.REDIS_HOST || 'localhost';
const REDIS_PORT = process.env.REDIS_PORT || 6379;

console.log(`🔗 Conectando ao Redis em ${REDIS_HOST}:${REDIS_PORT}`);

// Clientes Redis
const redisClient = redis.createClient({ socket: { host: REDIS_HOST, port: REDIS_PORT } });
const redisSubscriber = redisClient.duplicate();
let redisConnected = false;
const wsSubscribers = new Map();

// Conectar Redis
(async () => {
    try {
        await redisClient.connect();
        await redisSubscriber.connect();
        console.log('✅ Conectado ao Redis (Comandos e Pub/Sub)!');
        redisConnected = true;
    } catch (err) {
        console.log('❌ Erro ao conectar ao Redis:', err.message);
        redisConnected = false;
    }
})();

redisClient.on('error', (err) => console.log('❌ Redis Client Error:', err.message));
redisSubscriber.on('error', (err) => console.log('❌ Redis Subscriber Error:', err.message));

// Configurar WebSocket Server
const wss = new WebSocket.Server({ server, path: '/' });
console.log('🚀 Servidor MCP Redis WebSocket iniciando...');

wss.on('connection', (ws) => {
    console.log('✅ Nova conexão WebSocket estabelecida');

    ws.on('message', async (message) => {
        let data;
        let command = null;
        let args = [];
        try {
            data = JSON.parse(message);
            let response = { id: data.id, result: null, error: null, jsonrpc: '2.0' };

            if (data.method === 'redis.command' && data.params) {
                command = data.params.command;
                args = data.params.args || [];

                if (!redisConnected) {
                    response.error = { code: -32000, message: 'Servidor não conectado ao Redis' };
                    ws.send(JSON.stringify(response));
                    return;
                }

                switch (command.toLowerCase()) {
                    // ... (cases hgetall, hset, sadd, smembers, zadd, zincrby - permanecem os mesmos) ...
                    case 'hgetall':
                        try {
                            const result = await redisClient.hGetAll(args[0]);
                            const resultArray = Object.entries(result).flat();
                            response.result = resultArray;
                        } catch (err) {
                            console.error('❌ Redis HGETALL error:', err);
                            response.error = { code: -32603, message: err.message };
                        }
                        break;
                    case 'hset':
                        try {
                            const key = args[0];
                            const fields = args.slice(1);
                            const fieldsObj = {};
                            for (let i = 0; i < fields.length; i += 2) { fieldsObj[fields[i]] = fields[i + 1]; }
                            const result = await redisClient.hSet(key, fieldsObj);
                            response.result = result;
                            console.log(`✅ HSET ${key}:`, fieldsObj);
                        } catch (err) {
                            console.error('❌ Redis HSET error:', err);
                            response.error = { code: -32603, message: 'Redis error: ' + err.message };
                        }
                        break;
                    case 'sadd':
                        try {
                            const result = await redisClient.sAdd(args[0], args.slice(1));
                            response.result = result;
                            console.log(`✅ SADD ${args[0]}:`, args.slice(1));
                        } catch (err) {
                            console.error('❌ Redis SADD error:', err);
                            response.error = { code: -32603, message: 'Redis error: ' + err.message };
                        }
                        break;
                    case 'smembers':
                        try {
                            const result = await redisClient.sMembers(args[0]);
                            response.result = result;
                        } catch (err) {
                            console.error('❌ Redis SMEMBERS error:', err);
                            response.error = { code: -32603, message: err.message };
                        }
                        break;
                    case 'zadd':
                        try {
                            const key = args[0];
                            const members = [];
                            for (let i = 1; i < args.length; i += 2) { members.push({ score: parseFloat(args[i]), value: args[i + 1] }); }
                            const result = await redisClient.zAdd(key, members);
                            response.result = result;
                            console.log(`✅ ZADD ${key}:`, members);
                        } catch (err) {
                            console.error('❌ Redis ZADD error:', err);
                            response.error = { code: -32603, message: 'Redis error: ' + err.message };
                        }
                        break;
                    case 'zincrby':
                        try {
                            const result = await redisClient.zIncrBy(args[0], parseFloat(args[1]), args[2]);
                            response.result = result.toString();
                            console.log(`✅ ZINCRBY ${args[0]} ${args[1]} ${args[2]}:`, result);
                        } catch (err) {
                            console.error('❌ Redis ZINCRBY error:', err);
                            response.error = { code: -32603, message: 'Redis error: ' + err.message };
                        }
                        break;

                    // --- CORREÇÃO FINAL NO CASE 'ZRANGE' ---
                    case 'zrange':
                        try {
                            const key = args[0];
                            const min = args[1];
                            const max = args[2];
                            let withScores = args.includes('WITHSCORES');
                            let rev = args.includes('REV');

                            let redisResult;

                            if (withScores) {
                                // Usar zRangeWithScores que retorna [{ score: number, value: string }, ...]
                                console.log(`[SERVER DEBUG] Executing zRangeWithScores for ${key} (REV: ${rev})`);
                                redisResult = await redisClient.zRangeWithScores(key, min, max, { REV: rev });
                            } else {
                                // Usar zRange normal que retorna ["value1", "value2", ...]
                                console.log(`[SERVER DEBUG] Executing zRange for ${key} (REV: ${rev})`);
                                redisResult = await redisClient.zRange(key, min, max, { REV: rev });
                            }

                            console.log(`[SERVER DEBUG] Raw result from Redis client for ${key}:`, JSON.stringify(redisResult));
                            response.result = redisResult; // Enviar o resultado como está

                        } catch (err) {
                            console.error('❌ Redis ZRANGE/ZRANGEWITHSCORES error:', err);
                            response.error = { code: -32603, message: err.message };
                        }
                        break;
                    // --- FIM DA CORREÇÃO ---

                    // ... (cases xadd, subscribe, publish, xrange - permanecem os mesmos) ...
                    case 'xadd':
                        try {
                            const key = args[0];
                            const id = args[1];
                            const fields = {};
                            for (let i = 2; i < args.length; i += 2) { fields[args[i]] = args[i + 1]; }
                            const result = await redisClient.xAdd(key, id, fields);
                            response.result = result;
                            console.log(`✅ XADD ${key}:`, fields);
                        } catch (err) {
                            console.error('❌ Redis XADD error:', err);
                            response.error = { code: -32603, message: 'Redis error: ' + err.message };
                        }
                        break;
                    case 'subscribe':
                        try {
                            const channel = args[0];
                            if (!wsSubscribers.has(channel)) {
                                wsSubscribers.set(channel, new Set());
                                await redisSubscriber.subscribe(channel, (message, ch) => {
                                    console.log(`🔔 Mensagem recebida no canal ${ch}: ${message}`);
                                    const subscribers = wsSubscribers.get(ch);
                                    if (subscribers) {
                                        const notification = { jsonrpc: '2.0', method: 'redis.notification', params: { channel: ch, message: message } };
                                        const notificationStr = JSON.stringify(notification);
                                        subscribers.forEach(clientWs => { if (clientWs.readyState === WebSocket.OPEN) clientWs.send(notificationStr); });
                                    }
                                });
                                console.log(`🎧 Inscrito no canal Redis: ${channel}`);
                            }
                            wsSubscribers.get(channel).add(ws);
                            response.result = ['subscribe', channel, 1];
                        } catch (err) {
                            console.error('❌ Redis SUBSCRIBE error:', err);
                            response.error = { code: -32603, message: err.message };
                        }
                        break;
                    case 'publish':
                        try {
                            const channel = args[0];
                            const message = args[1];
                            const result = await redisClient.publish(channel, message);
                            response.result = result;
                            console.log(`📢 Publicado no canal ${channel}: ${message}`);
                        } catch (err) {
                            console.error('❌ Redis PUBLISH error:', err);
                            response.error = { code: -32603, message: err.message };
                        }
                        break;
                    case 'xrange':
                         try {
                            const result = await redisClient.xRange(args[0], args[1], args[2]);
                            const formattedResult = result.map(entry => [entry.id, Object.entries(entry.message).flat()]);
                            response.result = formattedResult;
                        } catch (err) {
                            console.error('❌ Redis XRANGE error:', err);
                            response.error = { code: -32603, message: err.message };
                        }
                        break;

                    default:
                        response.error = { code: -32601, message: `Comando desconhecido: ${command}` };
                } // Fim do switch
            } else {
                 response.error = { code: -32600, message: 'Requisição JSON-RPC inválida' };
            }

            // Log de debug anterior (mantido para referência, mas a correção está no case acima)
            if (command && command.toLowerCase() === 'zrange' && args.includes('WITHSCORES')) {
                 console.log('[SERVER DEBUG ZRANGE WITHSCORES] Response structure being sent:', JSON.stringify(response, null, 2));
            }

            ws.send(JSON.stringify(response));

        } catch (error) {
            console.error('❌ Erro ao processar mensagem:', error);
            ws.send(JSON.stringify({ id: data?.id || null, jsonrpc: '2.0', error: { message: error.message, code: -32700 } }));
        }
    });

    ws.on('close', () => {
        console.log('🔌 Conexão WebSocket fechada');
        wsSubscribers.forEach((clients, channel) => {
            if (clients.has(ws)) {
                clients.delete(ws);
                console.log(`🧹 Cliente removido do canal ${channel}`);
            }
        });
    });

    ws.send(JSON.stringify({ jsonrpc: '2.0', method: 'welcome', params: { message: 'Conectado ao servidor MCP Redis WebSocket', timestamp: Date.now() } }));
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`🎯 Servidor MCP Redis WebSocket rodando na porta ${PORT}`);
    console.log(`📡 WebSocket disponível em ws://localhost:${PORT}`);
});