#!/usr/bin/env python3
"""
Script de simulação de atividade para o CogniKids.

Funções:
- Busca usuários/turmas já criados (por email/nome)
- Cria uma coleção `devices` com 1 dispositivo por aluno
- Gera 100 leituras biométricas por aluno nos últimos 7 dias (coleção `iot_data`), com 5% de picos de estresse
- Gera 5 feelings por aluno nos últimos 7 dias (coleção `feelings`)
- Cria 2 desafios (coleção `challenges`) e 4 notas (coleção `grades`)
- Cria notificações para os pais baseadas nas notas (coleção `notifications`)
- Imprime contagem de documentos inseridos por coleção

Uso:
 py -3 scripts/simulate_activity.py

Observação: o script assume que as coleções `users` e `classes` já existem e contêm os registros criados pelo `populate_mongo.py`.
"""
import os
import sys
import random
import uuid
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId


def get_mongo_uri():
    return os.environ.get('MONGO_URI', 'mongodb://localhost:27017/cognikidsDB')


def rand_datetime_within(days=7):
    now = datetime.utcnow()
    delta_seconds = random.randint(0, days * 24 * 3600)
    return now - timedelta(seconds=delta_seconds)


def main():
    mongo_uri = get_mongo_uri()
    print(f"Conectando ao MongoDB em: {mongo_uri}")
    client = MongoClient(mongo_uri)
    db = client.get_default_database()

    # Buscar usuários e turmas de referência
    emails = {
        'carlos': 'carlos.antunes@escola.dev',
        'beatriz': 'beatriz.moreira@escola.dev',
        'ana': 'ana.sofia@aluno.dev',
        'bruno': 'bruno.costa@aluno.dev',
        'clara': 'clara.lima@aluno.dev',
        'diogo': 'diogo.mendes@aluno.dev',
        'ricardo': 'ricardo.alves@pais.dev',
        'mariana': 'mariana.costa@pais.dev',
        'helena': 'helena.mendes@pais.dev'
    }

    users = {}
    for key, email in emails.items():
        doc = db.users.find_one({"email": email})
        if not doc:
            print(f"ERRO: usuário com email {email} não encontrado. Execute populate_mongo.py primeiro.")
            sys.exit(1)
        users[key] = doc
        print(f"Encontrado {key}: {doc.get('_id')}")

    # Buscar turmas
    turma_301 = db.classes.find_one({"nome": "Turma 301 - Tarde"}) or db.classes.find_one({"name": "Turma 301 - Tarde"})
    turma_302 = db.classes.find_one({"nome": "Turma 302 - Manhã"}) or db.classes.find_one({"name": "Turma 302 - Manhã"})
    if not turma_301 or not turma_302:
        print("ERRO: turmas não encontradas. Execute populate_mongo.py primeiro.")
        sys.exit(1)
    print(f"Turma 301 id: {turma_301.get('_id')}")
    print(f"Turma 302 id: {turma_302.get('_id')}")

    # 1) Criar devices
    students = ['ana', 'bruno', 'clara', 'diogo']
    devices = {}
    device_docs = []
    for s in students:
        dispositivo_id = str(uuid.uuid4())
        student_id = users[s]['_id']
        doc = {
            'dispositivo_id': dispositivo_id,
            'student_id': ObjectId(student_id),
            'modelo': 'M5Stack Core2',
            'created_at': datetime.utcnow()
        }
        device_docs.append(doc)
        devices[s] = dispositivo_id

    if device_docs:
        res = db.devices.insert_many(device_docs)
        print(f"Inseridos {len(res.inserted_ids)} devices")

    # 2) Gerar iot_data (100 por aluno)
    print("Gerando iot_data...")
    iot_docs = []
    per_student = 100
    for s in students:
        dispositivo_id = devices[s]
        # selecionar índices de picos (5%)
        num_peaks = max(1, int(per_student * 0.05))
        peak_indices = set(random.sample(range(per_student), num_peaks))
        for i in range(per_student):
            ts = rand_datetime_within(7)
            if i in peak_indices:
                heart_rate = random.randint(110, 130)
                gsr = round(random.uniform(1.5, 2.5), 3)
            else:
                heart_rate = random.randint(65, 95)
                gsr = round(random.uniform(0.2, 1.0), 3)
            doc = {
                'dispositivo_id': dispositivo_id,
                'student_email': users[s]['email'],
                'student_id': ObjectId(users[s]['_id']),
                'timestamp_utc': ts,
                'dados_biometricos': {
                    'heart_rate': heart_rate,
                    'gsr': gsr
                }
            }
            iot_docs.append(doc)

    if iot_docs:
        # inserir em batch (por exemplo, em lotes de 500)
        batch_size = 500
        for i in range(0, len(iot_docs), batch_size):
            db.iot_data.insert_many(iot_docs[i:i+batch_size])
        print(f"Inseridos {len(iot_docs)} registros em 'iot_data'")

    # 3) Simular feelings (5 por aluno)
    print("Gerando feelings...")
    feelings_list = ["feliz", "neutro", "ansioso", "triste", "cansado"]
    feelings_docs = []
    per_student_feelings = 5
    for s in students:
        for _ in range(per_student_feelings):
            ts = rand_datetime_within(7)
            feeling = random.choice(feelings_list)
            comment = None
            if feeling in ['ansioso', 'triste']:
                comment = random.choice([
                    'Preciso conversar com o professor.',
                    'Senti dificuldade na atividade.',
                    'Hoje não estou bem.'
                ])
            doc = {
                'student_id': ObjectId(users[s]['_id']),
                'student_email': users[s]['email'],
                'feeling': feeling,
                'comment': comment,
                'timestamp': ts
            }
            feelings_docs.append(doc)

    if feelings_docs:
        db.feelings.insert_many(feelings_docs)
        print(f"Inseridos {len(feelings_docs)} registros em 'feelings'")

    # 4) Criar challenges (2)
    print("Criando challenges...")
    desafio1 = {
        'title': 'Desafio de Tabuada',
        'description': 'Resolver os exercícios de multiplicação da página 42.',
        'professor_id': ObjectId(users['carlos']['_id']),
        'class_id': turma_301['_id'],
        'dueDate': datetime.utcnow() + timedelta(days=7),
        'created_at': datetime.utcnow()
    }
    desafio2 = {
        'title': 'Projeto Feira de Ciências',
        'description': 'Entregar a primeira parte da pesquisa sobre o sistema solar.',
        'professor_id': ObjectId(users['beatriz']['_id']),
        'class_id': turma_302['_id'],
        'dueDate': datetime.utcnow() + timedelta(days=7),
        'created_at': datetime.utcnow()
    }
    res_ch = db.challenges.insert_many([desafio1, desafio2])
    desafio_tabuada_id, desafio_ciencias_id = res_ch.inserted_ids
    print(f"Criados challenges: {desafio_tabuada_id}, {desafio_ciencias_id}")

    # 5) Inserir grades
    print("Inserindo grades...")
    grades_docs = [
        {
            'student_id': ObjectId(users['ana']['_id']),
            'challenge_id': desafio_tabuada_id,
            'grade': 8.5,
            'subject': 'Matemática',
            'date': datetime.utcnow()
        },
        {
            'student_id': ObjectId(users['bruno']['_id']),
            'challenge_id': desafio_tabuada_id,
            'grade': 6.0,
            'subject': 'Matemática',
            'date': datetime.utcnow()
        },
        {
            'student_id': ObjectId(users['clara']['_id']),
            'challenge_id': desafio_ciencias_id,
            'grade': 9.5,
            'subject': 'Ciências',
            'date': datetime.utcnow()
        },
        {
            'student_id': ObjectId(users['diogo']['_id']),
            'challenge_id': desafio_ciencias_id,
            'grade': 7.0,
            'subject': 'Ciências',
            'date': datetime.utcnow()
        }
    ]
    res_gr = db.grades.insert_many(grades_docs)
    print(f"Inseridas {len(res_gr.inserted_ids)} grades")

    # 6) Notificações para pais
    print("Criando notifications para os pais...")
    notifications_docs = [
        {
            'user_id': ObjectId(users['ricardo']['_id']),
            'type': 'grade',
            'message': f"Ana Sofia recebeu a nota 8.5 em Matemática.",
            'read': False,
            'timestamp': datetime.utcnow()
        },
        {
            'user_id': ObjectId(users['mariana']['_id']),
            'type': 'grade',
            'message': f"Bruno Costa recebeu a nota 6.0 em Matemática.",
            'read': False,
            'timestamp': datetime.utcnow()
        },
        {
            'user_id': ObjectId(users['mariana']['_id']),
            'type': 'grade',
            'message': f"Clara Lima recebeu a nota 9.5 em Ciências.",
            'read': False,
            'timestamp': datetime.utcnow()
        },
        {
            'user_id': ObjectId(users['helena']['_id']),
            'type': 'grade',
            'message': f"Diogo Mendes recebeu a nota 7.0 em Ciências.",
            'read': False,
            'timestamp': datetime.utcnow()
        }
    ]
    res_not = db.notifications.insert_many(notifications_docs)
    print(f"Inseridas {len(res_not.inserted_ids)} notifications")

    # Resumo final: contagens por coleção
    summary = {
        'devices': db.devices.count_documents({}),
        'iot_data': db.iot_data.count_documents({}),
        'feelings': db.feelings.count_documents({}),
        'challenges': db.challenges.count_documents({}),
        'grades': db.grades.count_documents({}),
        'notifications': db.notifications.count_documents({})
    }
    print('\nSimulação concluída. Contagens atuais por coleção:')
    for k, v in summary.items():
        print(f" - {k}: {v}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Erro durante a simulação: {e}")
        sys.exit(1)
