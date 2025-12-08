"""
CogniKids - Script de Preparacao para Demonstracao
===================================================
Este script prepara o banco de dados com dados realistas para demonstracao.

Cria:
- Alunos na turma do Professor Carlos
- Dispositivos (pulseiras) associados aos alunos
- Alertas de crise recentes para aparecer no dashboard

Uso:
    python scripts/demos/preparar_demo.py
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import os

# Conexão com MongoDB (suporta execução local e dentro do Docker)
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
client = MongoClient(f"mongodb://{MONGO_HOST}:27017/")
db = client.cognikidsDB

# ============================================
# CONFIGURAÇÕES
# ============================================

# ID do Professor Carlos (fixo do banco)
PROFESSOR_CARLOS_ID = "69111874ca4398a1897afb9f"

# Alunos para criar (se não existirem)
ALUNOS = [
    {"nome": "Ana Sofia", "idade": 8, "email": "ana.sofia@aluno.cognikids.com"},
    {"nome": "Lucas Silva", "idade": 7, "email": "lucas.silva@aluno.cognikids.com"},
    {"nome": "Maria Clara", "idade": 9, "email": "maria.clara@aluno.cognikids.com"},
    {"nome": "Pedro Henrique", "idade": 8, "email": "pedro.henrique@aluno.cognikids.com"},
]

# Tipos de crise para demonstração
TIPOS_CRISE = [
    {
        "tipo": "Ansiedade Elevada",
        "severity": "high",
        "bpm_range": (140, 160),
        "gsr_range": (3.5, 5.0),
        "motivo": "Batimentos elevados + Alta condutância da pele"
    },
    {
        "tipo": "Estresse Agudo", 
        "severity": "high",
        "bpm_range": (150, 170),
        "gsr_range": (4.0, 5.5),
        "motivo": "Estado crítico - Batimentos e GSR extremos"
    },
    {
        "tipo": "Desconforto Moderado",
        "severity": "medium",
        "bpm_range": (120, 140),
        "gsr_range": (2.5, 3.5),
        "motivo": "Sinais de desconforto detectados"
    },
]


def limpar_alertas_antigos():
    """Remove alertas antigos (mais de 24h)"""
    ontem = datetime.utcnow() - timedelta(hours=24)
    resultado = db.alerts.delete_many({"data_hora": {"$lt": ontem}})
    print(f"[INFO] Removidos {resultado.deleted_count} alertas antigos")


def obter_ou_criar_turma_carlos():
    """Obtém ou cria uma turma do Professor Carlos"""
    turma = db.turmas.find_one({"professor_id": ObjectId(PROFESSOR_CARLOS_ID)})
    
    if not turma:
        turma_id = db.turmas.insert_one({
            "nome": "Turma A - 3º Ano",
            "professor_id": ObjectId(PROFESSOR_CARLOS_ID),
            "ano_letivo": "2025",
            "turno": "Manhã",
            "created_at": datetime.utcnow()
        }).inserted_id
        print(f"[OK] Turma criada: Turma A - 3º Ano")
        turma = db.turmas.find_one({"_id": turma_id})
    else:
        print(f"[OK] Turma existente: {turma.get('nome', 'Turma do Carlos')}")
    
    return turma


def obter_ou_criar_alunos(turma_id):
    """Obtém ou cria alunos na turma do Professor Carlos"""
    alunos_criados = []
    
    for aluno_data in ALUNOS:
        # Verifica se já existe
        aluno = db.users.find_one({
            "email": aluno_data["email"],
            "role": "aluno"
        })
        
        if not aluno:
            aluno_id = db.users.insert_one({
                "name": aluno_data["nome"],
                "email": aluno_data["email"],
                "password": "$2b$12$dummy",  # Não usado para alunos
                "role": "aluno",
                "idade": aluno_data["idade"],
                "turma_id": turma_id,
                "professor_id": ObjectId(PROFESSOR_CARLOS_ID),
                "created_at": datetime.utcnow()
            }).inserted_id
            print(f"  [OK] Aluno criado: {aluno_data['nome']}")
            aluno = {"_id": aluno_id, "name": aluno_data["nome"]}
        else:
            # Atualiza para garantir que está na turma certa
            db.users.update_one(
                {"_id": aluno["_id"]},
                {"$set": {
                    "turma_id": turma_id,
                    "professor_id": ObjectId(PROFESSOR_CARLOS_ID)
                }}
            )
            print(f"  [OK] Aluno existente: {aluno.get('name', aluno_data['nome'])}")
        
        alunos_criados.append(aluno)
    
    return alunos_criados


def criar_dispositivos(alunos):
    """Cria dispositivos (pulseiras) para os alunos"""
    dispositivos = []
    
    for aluno in alunos:
        # Verifica se já tem dispositivo
        dispositivo = db.dispositivos.find_one({"aluno_id": aluno["_id"]})
        
        if not dispositivo:
            disp_id = db.dispositivos.insert_one({
                "tipo": "pulseira_m5stack",
                "modelo": "M5StickC Plus",
                "aluno_id": aluno["_id"],
                "status": "ativo",
                "ultima_conexao": datetime.utcnow(),
                "created_at": datetime.utcnow()
            }).inserted_id
            dispositivo = {"_id": disp_id}
            print(f"  [OK] Dispositivo criado para {aluno.get('name', 'aluno')}")
        
        dispositivos.append({"aluno": aluno, "dispositivo": dispositivo})
    
    return dispositivos


def criar_alertas_crise(dispositivos):
    """Cria alertas de crise recentes para demonstração"""
    print("\n[INFO] Criando alertas de crise...")
    
    alertas_criados = 0
    
    # Seleciona 2 alunos aleatórios para ter alertas
    alunos_com_crise = random.sample(dispositivos, min(2, len(dispositivos)))
    
    for item in alunos_com_crise:
        aluno = item["aluno"]
        dispositivo = item["dispositivo"]
        
        # Escolhe tipo de crise aleatório
        crise = random.choice(TIPOS_CRISE)
        
        # Horário recente (últimas 2 horas)
        minutos_atras = random.randint(5, 120)
        data_hora = datetime.utcnow() - timedelta(minutes=minutos_atras)
        
        # Dados biométricos
        bpm = random.randint(*crise["bpm_range"])
        gsr = round(random.uniform(*crise["gsr_range"]), 1)
        
        # Cria o alerta
        db.alerts.insert_one({
            "aluno_id": aluno["_id"],
            "device_id": str(dispositivo["_id"]),
            "data_hora": data_hora,
            "alert_type": "crisis",
            "severity": crise["severity"],
            "dados_biometricos": {
                "bpm": bpm,
                "heart_rate": bpm,
                "gsr": gsr,
                "temperature": round(random.uniform(36.5, 37.5), 1)
            },
            "ml_confidence": round(random.uniform(0.85, 0.98), 2),
            "motivo": crise["motivo"],
            "created_at": data_hora,
            "lido": False,
            "resolvido": False
        })
        
        print(f"  [ALERTA] Alerta criado: {aluno.get('name', 'Aluno')} - {crise['tipo']}")
        print(f"      BPM: {bpm}, GSR: {gsr}, Há {minutos_atras} minutos")
        alertas_criados += 1
    
    return alertas_criados


def mostrar_resumo():
    """Mostra resumo dos dados no banco"""
    print("\n" + "=" * 50)
    print("RESUMO DO BANCO DE DADOS")
    print("=" * 50)
    
    # Conta registros
    users = db.users.count_documents({})
    alunos = db.users.count_documents({"role": "aluno"})
    turmas = db.turmas.count_documents({})
    dispositivos = db.dispositivos.count_documents({})
    alertas = db.alerts.count_documents({})
    alertas_recentes = db.alerts.count_documents({
        "data_hora": {"$gte": datetime.utcnow() - timedelta(hours=24)}
    })
    
    print(f"\n  Usuarios: {users} (incluindo {alunos} alunos)")
    print(f"  Turmas: {turmas}")
    print(f"  Dispositivos: {dispositivos}")
    print(f"  Alertas totais: {alertas}")
    print(f"  Alertas ultimas 24h: {alertas_recentes}")
    
    # Mostra alertas recentes
    print("\nALERTAS RECENTES:")
    alertas_list = list(db.alerts.find().sort("data_hora", -1).limit(5))
    for alerta in alertas_list:
        aluno = db.users.find_one({"_id": alerta.get("aluno_id")})
        nome = aluno.get("name", "Desconhecido") if aluno else "Desconhecido"
        data = alerta.get("data_hora", datetime.utcnow())
        severity = alerta.get("severity", "unknown")
        bpm = alerta.get("dados_biometricos", {}).get("bpm", 0)
        print(f"  - {nome}: BPM {bpm}, Severidade: {severity}, {data.strftime('%d/%m %H:%M')}")


def main():
    print("\n" + "=" * 50)
    print("COGNIKIDS - PREPARACAO PARA DEMONSTRACAO")
    print("=" * 50)
    
    # 1. Limpa alertas antigos
    print("\n[1] Limpando alertas antigos...")
    limpar_alertas_antigos()
    
    # 2. Obtém/cria turma do Professor Carlos
    print("\n[2] Configurando turma do Professor Carlos...")
    turma = obter_ou_criar_turma_carlos()
    
    # 3. Obtém/cria alunos
    print("\n[3] Configurando alunos...")
    alunos = obter_ou_criar_alunos(turma["_id"])
    
    # 4. Cria dispositivos
    print("\n[4] Configurando dispositivos (pulseiras)...")
    dispositivos = criar_dispositivos(alunos)
    
    # 5. Cria alertas de crise
    print("\n[5] Criando alertas de crise para demonstração...")
    alertas = criar_alertas_crise(dispositivos)
    
    # 6. Mostra resumo
    mostrar_resumo()
    
    print("\n" + "=" * 50)
    print("[OK] DEMONSTRACAO PREPARADA COM SUCESSO!")
    print("=" * 50)
    print("\nPara testar:")
    print("   1. Acesse o frontend: streamlit run app.py")
    print("   2. Login: carlos.antunes@escola.dev / senha123")
    print("   3. Veja os alertas de crise no dashboard")
    print("")


if __name__ == "__main__":
    main()
