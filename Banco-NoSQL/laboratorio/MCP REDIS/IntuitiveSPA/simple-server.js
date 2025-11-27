const WebSocket = require('ws');
const http = require('http');

console.log('🚀 Iniciando servidor WebSocket simples...');

// Criar servidor HTTP
const server = http.createServer();

// Criar servidor WebSocket
const wss = new WebSocket.Server({ 
    server,
    perMessageDeflate: false,
    // Permitir qualquer origem
    verifyClient: (info) => {
        console.log('🔍 Cliente tentando conectar:', info.origin);
        return true;
    }
});

// Dados mock para teste
const mockPolls = [
    {
        id: 'poll-1',
        question: 'Qual sua linguagem favorita?',
        options: [
            { id: 'opt1', text: 'JavaScript', votes: 45 },
            { id: 'opt2', text: 'Python', votes: 38 },
            { id: 'opt3', text: 'Java', votes: 25 }
        ],
        category: 'tech',
        createdAt: new Date().toISOString(),
        active: true
    }
];

let clients = [];

wss.on('connection', function connection(ws, request) {
    console.log('✅ Novo cliente conectado!');
    console.log('🌐 Origem:', request.headers.origin || 'Não especificada');
    console.log('👥 Total de clientes:', wss.clients.size);
    
    clients.push(ws);
    
    // Enviar dados iniciais
    setTimeout(() => {
        ws.send(JSON.stringify({
            jsonrpc: '2.0',
            id: 'init',
            result: {
                type: 'polls',
                data: mockPolls
            }
        }));
    }, 500);
    
    ws.on('message', function message(data) {
        console.log('📨 Mensagem recebida:', data.toString());
        
        try {
            const msg = JSON.parse(data);
            console.log('📋 Comando:', msg.method);
            
            // Resposta padrão de sucesso
            const response = {
                jsonrpc: '2.0',
                id: msg.id,
                result: {
                    success: true,
                    type: msg.method,
                    data: mockPolls
                }
            };
            
            ws.send(JSON.stringify(response));
            
            // Simular broadcast para outros clientes
            const broadcast = {
                jsonrpc: '2.0',
                method: 'notification',
                params: {
                    type: 'update',
                    data: mockPolls
                }
            };
            
            wss.clients.forEach(client => {
                if (client !== ws && client.readyState === WebSocket.OPEN) {
                    client.send(JSON.stringify(broadcast));
                }
            });
            
        } catch (error) {
            console.error('❌ Erro ao processar mensagem:', error);
            ws.send(JSON.stringify({
                jsonrpc: '2.0',
                id: 'error',
                error: {
                    code: -32603,
                    message: 'Erro interno do servidor'
                }
            }));
        }
    });
    
    ws.on('close', function close() {
        console.log('👋 Cliente desconectado');
        clients = clients.filter(client => client !== ws);
        console.log('👥 Clientes restantes:', clients.length);
    });
    
    ws.on('error', function error(err) {
        console.error('❌ Erro no WebSocket:', err);
    });
});

// Iniciar servidor
server.listen(3000, () => {
    console.log('🎯 Servidor WebSocket rodando na porta 3000');
    console.log('📡 WebSocket disponível em ws://localhost:3000');
    console.log('🔥 Pronto para receber conexões!');
});

// Log de status a cada 10 segundos
setInterval(() => {
    console.log(`📊 Status: ${wss.clients.size} clientes conectados`);
}, 10000);