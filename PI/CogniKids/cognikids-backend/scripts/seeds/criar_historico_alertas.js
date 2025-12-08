/**
 * Script para criar histórico de alertas para demonstração
 * Este script cria alertas dos últimos 30 dias para os alunos do Professor Carlos
 * BANCO: cognikidsDB
 */

// Busca TODOS os alunos (estudantes) do banco
let alunosInfo = [];
db.users.find({ tipo: "estudante" }).forEach(function(aluno) {
    alunosInfo.push({
        id: aluno._id,
        nome: aluno.nome
    });
});

print("Alunos encontrados: " + alunosInfo.length);

// Motivos de crise possíveis
const motivos = [
    "Batimento cardíaco elevado durante atividade",
    "Nível de stress detectado acima do normal",
    "Padrão de ansiedade identificado",
    "Frequência cardíaca irregular",
    "Sinais de desconforto emocional",
    "Resposta galvânica da pele elevada",
    "Combinação de BPM alto e stress elevado"
];

// Função para gerar data aleatória nos últimos N dias
function randomDate(daysBack) {
    const now = new Date();
    const pastDate = new Date(now.getTime() - (Math.random() * daysBack * 24 * 60 * 60 * 1000));
    return pastDate;
}

// Função para gerar BPM realístico
function randomBPM(severity) {
    if (severity === 'high') {
        return 145 + Math.random() * 25; // 145-170
    } else if (severity === 'medium') {
        return 130 + Math.random() * 15; // 130-145
    } else {
        return 110 + Math.random() * 20; // 110-130
    }
}

// Função para gerar GSR realístico
function randomGSR(severity) {
    if (severity === 'high') {
        return 2.0 + Math.random() * 1.0; // 2.0-3.0
    } else if (severity === 'medium') {
        return 1.5 + Math.random() * 0.5; // 1.5-2.0
    } else {
        return 1.0 + Math.random() * 0.5; // 1.0-1.5
    }
}

// Limpa alertas antigos (exceto os recentes de demonstração)
print("Limpando alertas antigos de demonstração...");
db.alerts.deleteMany({ demo: true });

// Cria alertas históricos
let alertasCriados = 0;

alunosInfo.forEach(function(aluno, alunoIdx) {
    // Cada aluno terá entre 3 e 8 alertas nos últimos 30 dias
    const numAlertas = 3 + Math.floor(Math.random() * 6);
    
    for (let i = 0; i < numAlertas; i++) {
        const severities = ['low', 'medium', 'high'];
        const severity = severities[Math.floor(Math.random() * severities.length)];
        
        const alerta = {
            student_id: aluno.id,
            student_name: aluno.nome,
            data_hora: randomDate(30),
            severity: severity,
            bpm: randomBPM(severity),
            gsr: randomGSR(severity),
            motivo: motivos[Math.floor(Math.random() * motivos.length)],
            resolvido: Math.random() > 0.3, // 70% resolvidos
            resolved_at: null,
            created_at: new Date(),
            demo: true // Marcador para poder limpar depois
        };
        
        // Se resolvido, adiciona data de resolução
        if (alerta.resolvido) {
            alerta.resolved_at = new Date(alerta.data_hora.getTime() + (Math.random() * 60 * 60 * 1000)); // até 1h depois
        }
        
        db.alerts.insertOne(alerta);
        alertasCriados++;
    }
    
    print("Criados " + numAlertas + " alertas para: " + aluno.nome);
});

print("\n=== RESUMO ===");
print("Total de alertas criados: " + alertasCriados);
print("Total de alunos com alertas: " + alunosInfo.length);

// Verifica a criação
print("\n=== VERIFICAÇÃO ===");
let totalAlertas = db.alerts.countDocuments({ demo: true });
print("Alertas na collection 'alerts': " + totalAlertas);

// Mostra alguns exemplos
print("\n=== EXEMPLOS DE ALERTAS ===");
db.alerts.find({ demo: true }).limit(3).forEach(function(a) {
    print("  - " + a.student_name + ": " + a.severity + " | BPM: " + a.bpm.toFixed(1) + " | " + a.data_hora);
});
