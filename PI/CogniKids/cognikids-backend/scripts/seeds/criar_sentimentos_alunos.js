// Script para criar sentimentos para os alunos do Professor Carlos
// Segue o padrão da coleção feelings

var carlosId = ObjectId('69111874ca4398a1897afb9f');

// Lista de sentimentos possíveis
var sentimentos = ['feliz', 'animado', 'neutro', 'cansado', 'triste', 'ansioso'];

// Função para gerar data aleatória nos últimos 7 dias
function randomDate(dias) {
    var now = new Date();
    var offset = Math.floor(Math.random() * dias * 24 * 60 * 60 * 1000);
    return new Date(now.getTime() - offset);
}

// Função para escolher sentimento aleatório (com pesos)
function randomSentimento() {
    var pesos = {
        'feliz': 25,
        'animado': 15,
        'neutro': 30,
        'cansado': 15,
        'triste': 8,
        'ansioso': 7
    };
    
    var total = 0;
    for (var s in pesos) total += pesos[s];
    
    var rand = Math.floor(Math.random() * total);
    var acum = 0;
    
    for (var s in pesos) {
        acum += pesos[s];
        if (rand < acum) return s;
    }
    return 'neutro';
}

print('=== CRIANDO SENTIMENTOS PARA ALUNOS DO PROFESSOR CARLOS ===\n');

// Buscar todas as turmas do professor
var turmas = db.turmas.find({teacher_id: carlosId}).toArray();

var totalSentimentos = 0;

turmas.forEach(function(turma) {
    print('[TURMA] ' + turma.nome + ':');
    
    var alunosIds = turma.alunos_ids || [];
    
    alunosIds.forEach(function(alunoId) {
        var aluno = db.users.findOne({_id: alunoId});
        if (!aluno) return;
        
        // Criar 3-5 registros de sentimento por aluno (últimos 7 dias)
        var qtd = 3 + Math.floor(Math.random() * 3);
        
        for (var i = 0; i < qtd; i++) {
            var sentimento = randomSentimento();
            var data = randomDate(7);
            
            db.feelings.insertOne({
                aluno_id: alunoId,
                student_id: alunoId,
                sentimento: sentimento,
                feeling: sentimento,
                data: data,
                created_at: data,
                turma_id: turma._id,
                observacao: ''
            });
            
            totalSentimentos++;
        }
        
        print('  OK: ' + aluno.nome + ': ' + qtd + ' sentimentos');
    });
    
    print('');
});

print('=== RESUMO ===');
print('Total de sentimentos criados: ' + totalSentimentos);

// Estatísticas
print('\n[DISTRIBUICAO] Distribuicao de sentimentos:');
sentimentos.forEach(function(s) {
    var count = db.feelings.countDocuments({sentimento: s});
    print('  ' + s + ': ' + count);
});
