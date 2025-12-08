#!/usr/bin/env python3
"""
Script para popular o MongoDB com dados de teste para o projeto CogniKids.

Este script faz o seguinte, na ordem:
 - Limpa as coleções `users` e `classes`
 - Define senha_plana = "senha123" e gera um hash bcrypt (campo `senha`)
 - Insere 2 professores, 2 turmas, 4 alunos e 3 pais
 - Atualiza relações: pais -> filhos (filhos_ids), professores -> turmas (turmas_ids), e matricula alunos nas turmas (classes.students)
 - Gera o arquivo `novos_logins.txt` no formato solicitado

Uso:
 - Certifique-se de que o MongoDB está acessível (por padrão: mongodb://localhost:27017)
 - Rode: python scripts/populate_mongo.py
"""
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import sys


def get_mongo_uri():
    # Prioriza variável de ambiente MONGO_URI, senão usa o padrão local
    return os.environ.get('MONGO_URI', 'mongodb://localhost:27017/cognikidsDB')


def main():
    mongo_uri = get_mongo_uri()
    print(f"Conectando ao MongoDB em: {mongo_uri}")
    client = MongoClient(mongo_uri)
    db = client.get_default_database()

    # 1) Limpar coleções
    print("Limpando coleções 'users' e 'classes'...")
    db.users.delete_many({})
    db.classes.delete_many({})

    # 2) Definir senha plana e hash
    senha_plana = "senha123"
    hashed = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed.decode('utf-8')
    print("Senha hash gerada (bcrypt).")

    # Helper para criar usuário
    def create_user(nome, email, tipo, extra_fields=None):
        user = {
            "nome": nome,
            "email": email,
            "senha": hashed_password,
            "tipo": tipo
        }
        if extra_fields:
            user.update(extra_fields)
        res = db.users.insert_one(user)
        print(f"Inserido usuário {nome} -> {res.inserted_id}")
        return res.inserted_id

    # 3) Criar Professores
    prof_carlos_id = create_user("Prof. Carlos Antunes", "carlos.antunes@escola.dev", "professor")
    prof_beatriz_id = create_user("Profa. Beatriz Moreira", "beatriz.moreira@escola.dev", "professor")

    # 4) Criar Turmas (collection: classes)
    # Para compatibilidade com o projeto, vamos criar campos em inglês (esperados por class_model)
    turma_301 = {
        "name": "Turma 301 - Tarde",
        "grade": "301",
        "section": "Tarde",
        "teacher_id": ObjectId(prof_carlos_id),
        "school_year": 2025,
        "students": [],
        # campos em português solicitados pelo prompt
        "nome": "Turma 301 - Tarde",
        "ano_letivo": 2025,
        "professor_id": ObjectId(prof_carlos_id)
    }
    turma_302 = {
        "name": "Turma 302 - Manhã",
        "grade": "302",
        "section": "Manha",
        "teacher_id": ObjectId(prof_beatriz_id),
        "school_year": 2025,
        "students": [],
        "nome": "Turma 302 - Manhã",
        "ano_letivo": 2025,
        "professor_id": ObjectId(prof_beatriz_id)
    }
    res301 = db.classes.insert_one(turma_301)
    turma_301_id = res301.inserted_id
    print(f"Inserida Turma 301 -> {turma_301_id}")
    res302 = db.classes.insert_one(turma_302)
    turma_302_id = res302.inserted_id
    print(f"Inserida Turma 302 -> {turma_302_id}")

    # 5) Criar Alunos
    ana_id = create_user("Ana Sofia", "ana.sofia@aluno.dev", "estudante", {"turma_id": ObjectId(turma_301_id)})
    bruno_id = create_user("Bruno Costa", "bruno.costa@aluno.dev", "estudante", {"turma_id": ObjectId(turma_301_id)})
    clara_id = create_user("Clara Lima", "clara.lima@aluno.dev", "estudante", {"turma_id": ObjectId(turma_302_id)})
    diogo_id = create_user("Diogo Mendes", "diogo.mendes@aluno.dev", "estudante", {"turma_id": ObjectId(turma_302_id)})

    # Matricular alunos nas turmas: adicionar aos arrays classes.students
    print("Matriculando alunos nas turmas...")
    db.classes.update_one({"_id": turma_301_id}, {"$addToSet": {"students": ObjectId(ana_id)}})
    db.classes.update_one({"_id": turma_301_id}, {"$addToSet": {"students": ObjectId(bruno_id)}})
    db.classes.update_one({"_id": turma_302_id}, {"$addToSet": {"students": ObjectId(clara_id)}})
    db.classes.update_one({"_id": turma_302_id}, {"$addToSet": {"students": ObjectId(diogo_id)}})

    # 6) Criar Pais
    ricardo_id = create_user("Ricardo Alves (Pai)", "ricardo.alves@pais.dev", "pai")
    mariana_id = create_user("Mariana Costa (Mãe)", "mariana.costa@pais.dev", "pai")
    helena_id = create_user("Helena Mendes (Mãe)", "helena.mendes@pais.dev", "pai")

    # 7) Atualizar relações Pais -> Filhos (filhos_ids)
    print("Atualizando relações pais -> filhos...")
    db.users.update_one({"_id": ricardo_id}, {"$set": {"filhos_ids": [ObjectId(ana_id)]}})
    db.users.update_one({"_id": mariana_id}, {"$set": {"filhos_ids": [ObjectId(bruno_id), ObjectId(clara_id)]}})
    db.users.update_one({"_id": helena_id}, {"$set": {"filhos_ids": [ObjectId(diogo_id)]}})

    # 8) Atualizar Professores -> Turmas (turmas_ids)
    print("Atualizando relações professores -> turmas...")
    db.users.update_one({"_id": prof_carlos_id}, {"$set": {"turmas_ids": [ObjectId(turma_301_id)]}})
    db.users.update_one({"_id": prof_beatriz_id}, {"$set": {"turmas_ids": [ObjectId(turma_302_id)]}})

    # Resultado: mostrar IDs gerados
    print("\nResumo dos IDs gerados:")
    print(f"prof_carlos_id: {prof_carlos_id}")
    print(f"prof_beatriz_id: {prof_beatriz_id}")
    print(f"turma_301_id: {turma_301_id}")
    print(f"turma_302_id: {turma_302_id}")
    print(f"ana_id: {ana_id}")
    print(f"bruno_id: {bruno_id}")
    print(f"clara_id: {clara_id}")
    print(f"diogo_id: {diogo_id}")
    print(f"ricardo_id: {ricardo_id}")
    print(f"mariana_id: {mariana_id}")
    print(f"helena_id: {helena_id}")

    # 9) Gerar arquivo novos_logins.txt
    print("Gerando arquivo 'novos_logins.txt'...")
    content_lines = [
        "# Logins CogniKids (Senha Padrão: senha123)",
        "Professores",
        "Tipo: Professor",
        "",
        "Nome: Prof. Carlos Antunes",
        "",
        "Email: carlos.antunes@escola.dev",
        "",
        "Tipo: Professor",
        "",
        "Nome: Profa. Beatriz Moreira",
        "",
        "Email: beatriz.moreira@escola.dev",
        "",
        "Pais/Responsáveis",
        "Tipo: Pai/Responsável",
        "",
        "Nome: Ricardo Alves (Pai)",
        "",
        "Email: ricardo.alves@pais.dev",
        "",
        "Tipo: Pai/Responsável",
        "",
        "Nome: Mariana Costa (Mãe)",
        "",
        "Email: mariana.costa@pais.dev",
        "",
        "Tipo: Pai/Responsável",
        "",
        "Nome: Helena Mendes (Mãe)",
        "",
        "Email: helena.mendes@pais.dev",
        "",
        "Alunos",
        "Tipo: Aluno",
        "",
        "Nome: Ana Sofia",
        "",
        "Email: ana.sofia@aluno.dev",
        "",
        "Tipo: Aluno",
        "",
        "Nome: Bruno Costa",
        "",
        "Email: bruno.costa@aluno.dev",
        "",
        "Tipo: Aluno",
        "",
        "Nome: Clara Lima",
        "",
        "Email: clara.lima@aluno.dev",
        "",
        "Tipo: Aluno",
        "",
        "Nome: Diogo Mendes",
        "",
        "Email: diogo.mendes@aluno.dev",
    ]

    with open('novos_logins.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_lines))

    print("Arquivo 'novos_logins.txt' criado com sucesso.")
    print("Script finalizado.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Erro ao executar o script: {e}")
        sys.exit(1)
