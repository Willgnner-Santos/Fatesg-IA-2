"""
Script de Demonstração - Geração de Alertas de Crise em Tempo Real
====================================================================
Use este script durante sua apresentação para simular alertas de crise
e demonstrar o sistema de monitoramento funcionando.

Uso:
    python demo_alertas_apresentacao.py
    
O script vai:
1. Gerar dados IoT simulados (batimentos cardíacos e GSR elevados)
2. Inserir na coleção 'alerts' (Data Mart)
3. Os alertas aparecerão automaticamente no dashboard do professor
"""

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import random
import time

# Cores para output no terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}[INFO] {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}[AVISO] {text}{Colors.ENDC}")

def print_alert(text):
    print(f"{Colors.FAIL}[ALERTA] {text}{Colors.ENDC}")

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cognikidsDB"]

# IDs dos alunos do Professor Carlos Antunes
ALUNOS = [
    {
        'id': ObjectId("69111874ca4398a1897afba3"),
        'nome': 'Ana Sofia',
        'device_id': 'pulseira_ana_001'
    },
    {
        'id': ObjectId("69111874ca4398a1897afba4"),
        'nome': 'Lucas Silva',
        'device_id': 'pulseira_lucas_002'
    }
]

# Tipos de crise para demonstração
TIPOS_CRISE = [
    {
        'tipo': 'Ansiedade Severa',
        'hr_range': (130, 150),
        'gsr_range': (2.0, 3.5),
        'descricao': 'Batimentos elevados + Alta condutância da pele'
    },
    {
        'tipo': 'Estresse Intenso',
        'hr_range': (140, 160),
        'gsr_range': (2.5, 4.0),
        'descricao': 'Batimentos muito altos + Sudorese intensa'
    },
    {
        'tipo': 'Possível Ataque de Pânico',
        'hr_range': (150, 170),
        'gsr_range': (3.0, 5.0),
        'descricao': 'Estado crítico - Batimentos e GSR extremos'
    }
]

def gerar_alerta_crise(aluno, tipo_crise):
    """
    Gera um alerta de crise realista para demonstração.
    """
    hr_value = random.uniform(tipo_crise['hr_range'][0], tipo_crise['hr_range'][1])
    gsr_value = random.uniform(tipo_crise['gsr_range'][0], tipo_crise['gsr_range'][1])
    
    # IMPORTANTE: Usar datetime.utcnow() para compatibilidade com o backend
    timestamp = datetime.utcnow()
    
    alerta = {
        'aluno_id': aluno['id'],  # Campo correto para o backend
        'student_id': aluno['id'],  # Campo adicional para compatibilidade
        'device_id': aluno['device_id'],
        'data_hora': timestamp,  # Campo correto para o backend (UTC!)
        'alert_type': 'crisis',
        'severity': 'high',
        'bpm': round(hr_value, 1),
        'gsr': round(gsr_value, 2),
        'movement_score': round(random.uniform(0.2, 0.8), 2),  # Baixo movimento indica crise
        'dados_biometricos': {
            'bpm': round(hr_value, 1),
            'heart_rate': round(hr_value, 1),
            'gsr': round(gsr_value, 2),
            'movement_score': round(random.uniform(0.2, 0.8), 2),
            'temperature': round(random.uniform(36.5, 37.2), 1)
        },
        'ml_confidence': round(random.uniform(0.85, 0.98), 2),
        'motivo': tipo_crise['descricao'],
        'created_at': timestamp,
        'resolvido': False,
        'lido': False
    }
    
    return alerta

def limpar_alertas_antigos():
    """Remove alertas antigos para começar a demo limpa."""
    resultado = db.alerts.delete_many({
        'data_hora': {'$lt': datetime.utcnow() - timedelta(minutes=10)}
    })
    if resultado.deleted_count > 0:
        print_info(f"Limpou {resultado.deleted_count} alertas antigos (>10 min)")

def cenario_1_alerta_unico():
    """Cenário 1: Um aluno com crise de ansiedade."""
    print_header("CENÁRIO 1: Alerta Único - Ansiedade")
    
    aluno = ALUNOS[0]  # Ana Sofia
    tipo = TIPOS_CRISE[0]  # Ansiedade Severa
    
    print_info(f"Simulando crise para: {aluno['nome']}")
    print_info(f"Tipo: {tipo['tipo']}")
    
    alerta = gerar_alerta_crise(aluno, tipo)
    db.alerts.insert_one(alerta)
    
    print_alert(f"ALERTA DE CRISE GERADO!")
    print(f"   Aluno: {aluno['nome']}")
    print(f"   Batimentos: {alerta['dados_biometricos']['bpm']} bpm")
    print(f"   GSR: {alerta['dados_biometricos']['gsr']}")
    print(f"   Confianca ML: {alerta['ml_confidence']*100}%")
    print_success(f"Alerta inserido na coleção 'alerts'")
    print_warning("Atualize o dashboard do professor para ver o alerta!")

def cenario_2_multiplos_alertas():
    """Cenário 2: Dois alunos com crises simultâneas."""
    print_header("CENÁRIO 2: Múltiplos Alertas - Sala em Crise")
    
    alertas_inseridos = []
    
    for i, aluno in enumerate(ALUNOS):
        tipo = TIPOS_CRISE[i]  # Cada aluno com tipo diferente
        
        print_info(f"Simulando crise para: {aluno['nome']} ({tipo['tipo']})")
        
        alerta = gerar_alerta_crise(aluno, tipo)
        db.alerts.insert_one(alerta)
        alertas_inseridos.append(alerta)
        
        print_alert(f"{aluno['nome']}: {tipo['tipo']}")
        print(f"   HR: {alerta['dados_biometricos']['bpm']} bpm | GSR: {alerta['dados_biometricos']['gsr']}")
        
        time.sleep(1)  # Pausa dramática para apresentação
    
    print_success(f"\n{len(alertas_inseridos)} alertas críticos gerados!")
    print_warning("Dashboard mostrará MÚLTIPLOS ALUNOS EM CRISE!")

def cenario_3_escalada_crise():
    """Cenário 3: Crise que piora progressivamente."""
    print_header("CENÁRIO 3: Escalada de Crise - Piora Progressiva")
    
    aluno = ALUNOS[1]  # Lucas Silva
    
    print_info(f"Simulando escalada de crise para: {aluno['nome']}")
    print_info("A crise vai piorar em 3 estágios...\n")
    
    for i, tipo in enumerate(TIPOS_CRISE):
        print(f"\n{Colors.WARNING}ESTAGIO {i+1}/3: {tipo['tipo']}{Colors.ENDC}")
        
        alerta = gerar_alerta_crise(aluno, tipo)
        db.alerts.insert_one(alerta)
        
        print_alert(f"Metricas agravadas!")
        print(f"   Batimentos: {alerta['dados_biometricos']['bpm']} bpm")
        print(f"   GSR: {alerta['dados_biometricos']['gsr']}")
        
        if i < len(TIPOS_CRISE) - 1:
            print_info("Aguardando 3 segundos antes do próximo estágio...")
            time.sleep(3)
    
    print_success(f"\nEscalada completa! {len(TIPOS_CRISE)} alertas progressivos gerados")
    print_warning("Dashboard mostrará histórico de piora do aluno!")

def cenario_4_fluxo_continuo():
    """Cenário 4: Fluxo contínuo de alertas para demonstração dinâmica."""
    print_header("CENÁRIO 4: Demo Dinâmica - Fluxo Contínuo")
    
    print_info("Gerando alertas a cada 5 segundos...")
    print_warning("Pressione Ctrl+C para parar\n")
    
    contador = 0
    try:
        while True:
            contador += 1
            
            # Alterna entre alunos
            aluno = random.choice(ALUNOS)
            tipo = random.choice(TIPOS_CRISE)
            
            alerta = gerar_alerta_crise(aluno, tipo)
            db.alerts.insert_one(alerta)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print_alert(f"[{timestamp}] #{contador} - {aluno['nome']}: {tipo['tipo']}")
            print(f"   {alerta['dados_biometricos']['bpm']} bpm | GSR {alerta['dados_biometricos']['gsr']}")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.OKGREEN}[OK] Demo finalizada! Total de alertas gerados: {contador}{Colors.ENDC}")

def verificar_alertas_dashboard():
    """Mostra quantos alertas o dashboard está vendo agora."""
    print_header("Verificação de Alertas Visíveis no Dashboard")
    
    # Alertas dos últimos 5 minutos (mesma lógica do backend - UTC!)
    cinco_min_atras = datetime.utcnow() - timedelta(minutes=5)
    
    alertas_recentes = list(db.alerts.find({
        'aluno_id': {'$in': [a['id'] for a in ALUNOS]},
        'data_hora': {'$gte': cinco_min_atras}
    }).sort('data_hora', -1))
    
    if not alertas_recentes:
        print_warning("Nenhum alerta nos últimos 5 minutos")
        print_info("Execute um dos cenários acima para gerar alertas!")
    else:
        print_success(f"Encontrados {len(alertas_recentes)} alertas ativos (últimos 5 min)")
        
        # Agrupa por aluno
        por_aluno = {}
        for alerta in alertas_recentes:
            aluno_id = str(alerta['aluno_id'])
            if aluno_id not in por_aluno:
                por_aluno[aluno_id] = []
            por_aluno[aluno_id].append(alerta)
        
        print(f"\n{Colors.BOLD}Resumo por Aluno:{Colors.ENDC}")
        for aluno in ALUNOS:
            aluno_id = str(aluno['id'])
            if aluno_id in por_aluno:
                qtd = len(por_aluno[aluno_id])
                ultimo = por_aluno[aluno_id][0]
                tempo = int((datetime.utcnow() - ultimo['data_hora']).total_seconds())
                dados = ultimo.get('dados_biometricos', {})
                print_alert(f"  {aluno['nome']}: {qtd} alerta(s) - ultimo ha {tempo}s")
                print(f"      {dados.get('bpm', 'N/A')} bpm | GSR {dados.get('gsr', 'N/A')}")
            else:
                print_success(f"  {aluno['nome']}: Sem alertas")

def menu_principal():
    """Menu interativo para escolher o cenário de demonstração."""
    print_header("DEMO - Sistema de Alertas de Crise CogniKids")
    
    print(f"{Colors.BOLD}Escolha um cenário de demonstração:{Colors.ENDC}\n")
    print(f"{Colors.OKCYAN}1{Colors.ENDC} - Alerta Único (1 aluno com ansiedade)")
    print(f"{Colors.OKCYAN}2{Colors.ENDC} - Múltiplos Alertas (2 alunos em crise simultânea)")
    print(f"{Colors.OKCYAN}3{Colors.ENDC} - Escalada de Crise (piora progressiva)")
    print(f"{Colors.OKCYAN}4{Colors.ENDC} - Fluxo Contínuo (demo dinâmica)")
    print(f"{Colors.OKCYAN}5{Colors.ENDC} - Verificar Alertas Atuais")
    print(f"{Colors.OKCYAN}6{Colors.ENDC} - Limpar Alertas Antigos")
    print(f"{Colors.FAIL}0{Colors.ENDC} - Sair")
    
    escolha = input(f"\n{Colors.BOLD}Digite o número do cenário: {Colors.ENDC}")
    
    if escolha == '1':
        limpar_alertas_antigos()
        cenario_1_alerta_unico()
    elif escolha == '2':
        limpar_alertas_antigos()
        cenario_2_multiplos_alertas()
    elif escolha == '3':
        limpar_alertas_antigos()
        cenario_3_escalada_crise()
    elif escolha == '4':
        limpar_alertas_antigos()
        cenario_4_fluxo_continuo()
    elif escolha == '5':
        verificar_alertas_dashboard()
    elif escolha == '6':
        limpar_alertas_antigos()
        print_success("Alertas antigos removidos!")
    elif escolha == '0':
        print_success("Até logo!")
        return False
    else:
        print_warning("Opção inválida!")
    
    input(f"\n{Colors.BOLD}Pressione ENTER para voltar ao menu...{Colors.ENDC}")
    return True

if __name__ == "__main__":
    try:
        while True:
            continuar = menu_principal()
            if not continuar:
                break
    except KeyboardInterrupt:
        print(f"\n\n{Colors.OKGREEN}[OK] Demo encerrada!{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}[ERRO] {e}{Colors.ENDC}")
