import pymongo  
from transformers import pipeline
import torch
import pandas as pd
from datetime import datetime
import re

# Conectar ao MongoDB
client = pymongo.MongoClient("")  

db = client["startup"]  

# Coleção com dados dos funcionários
collection_funcionarios = db["funcionarios"]

# Coleção para armazenar os resultados
collection_resultados = db["resultados_ia"]

print("="*80)
print("SISTEMA DE GERAÇÃO E RESPOSTA DE PERGUNTAS COM IA (OPT-IML-1.3B)")
print("="*80)

# PASSO 1: Extrair dados dos funcionários do MongoDB
print("\n📥 Passo 1: Buscando dados dos funcionários no MongoDB...")
funcionarios = list(collection_funcionarios.find().limit(15))
print(f"✓ Total de {len(funcionarios)} funcionários encontrados")

# PASSO 2: Formatar os dados em um texto legível
print("\n📋 Passo 2: Formatando dados para análise...")
dados_formatados = "DADOS DOS FUNCIONÁRIOS:\n\n"
for i, func in enumerate(funcionarios, 1):
    nome = func.get('nome', 'N/A')
    idade = func.get('idade', 'N/A')
    salario = func.get('salario', 'N/A')
    posicao = func.get('posicao', 'N/A')
    departamento = func.get('departamento', 'N/A')
    
    dados_formatados += f"{i}. {nome} - {idade} anos - R$ {salario:.2f} - {posicao} - {departamento}\n"

print("✓ Dados formatados com sucesso")
print(f"\nContexto:\n{dados_formatados}\n")

# PASSO 3: Carregar modelo OPT-IML-1.3B
print("🤖 Passo 3: Carregando modelo facebook/opt-iml-1.3b...")
try:
    modelo_ia = pipeline("text-generation", model="facebook/opt-iml-1.3b", 
                         device=0 if torch.cuda.is_available() else -1,
                         trust_remote_code=True)
    print("✓ Modelo facebook/opt-iml-1.3b carregado com sucesso")
except Exception as e:
    print(f"⚠ Erro: {e}")
    modelo_ia = pipeline("text-generation", model="facebook/opt-iml-1.3b", device=-1)

# PASSO 4: Gerar perguntas
print("\n🔄 Passo 4: Gerando perguntas com IA...\n")

prompt_perguntas = f"""{dados_formatados}

Gere 5 perguntas sobre os dados acima:
Pergunta 1:"""

try:
    print("⏳ Gerando Pergunta 1...")
    resultado1 = modelo_ia(prompt_perguntas, max_new_tokens=100, do_sample=True, 
                           temperature=0.7, top_p=0.9, truncation=True)
    pergunta1 = resultado1[0]['generated_text'].split("Pergunta 1:")[-1].strip().split('\n')[0]
    print(f"✓ P1: {pergunta1}\n")
except Exception as e:
    pergunta1 = "Erro ao gerar"
    print(f"✗ Erro: {e}\n")

try:
    print("⏳ Gerando Pergunta 2...")
    prompt2 = f"{dados_formatados}\nPergunta 2:"
    resultado2 = modelo_ia(prompt2, max_new_tokens=100, do_sample=True, 
                           temperature=0.7, top_p=0.9, truncation=True)
    pergunta2 = resultado2[0]['generated_text'].split("Pergunta 2:")[-1].strip().split('\n')[0]
    print(f"✓ P2: {pergunta2}\n")
except Exception as e:
    pergunta2 = "Erro ao gerar"
    print(f"✗ Erro: {e}\n")

try:
    print("⏳ Gerando Pergunta 3...")
    prompt3 = f"{dados_formatados}\nPergunta 3:"
    resultado3 = modelo_ia(prompt3, max_new_tokens=100, do_sample=True, 
                           temperature=0.7, top_p=0.9, truncation=True)
    pergunta3 = resultado3[0]['generated_text'].split("Pergunta 3:")[-1].strip().split('\n')[0]
    print(f"✓ P3: {pergunta3}\n")
except Exception as e:
    pergunta3 = "Erro ao gerar"
    print(f"✗ Erro: {e}\n")

try:
    print("⏳ Gerando Pergunta 4...")
    prompt4 = f"{dados_formatados}\nPergunta 4:"
    resultado4 = modelo_ia(prompt4, max_new_tokens=100, do_sample=True, 
                           temperature=0.7, top_p=0.9, truncation=True)
    pergunta4 = resultado4[0]['generated_text'].split("Pergunta 4:")[-1].strip().split('\n')[0]
    print(f"✓ P4: {pergunta4}\n")
except Exception as e:
    pergunta4 = "Erro ao gerar"
    print(f"✗ Erro: {e}\n")

try:
    print("⏳ Gerando Pergunta 5...")
    prompt5 = f"{dados_formatados}\nPergunta 5:"
    resultado5 = modelo_ia(prompt5, max_new_tokens=100, do_sample=True, 
                           temperature=0.7, top_p=0.9, truncation=True)
    pergunta5 = resultado5[0]['generated_text'].split("Pergunta 5:")[-1].strip().split('\n')[0]
    print(f"✓ P5: {pergunta5}\n")
except Exception as e:
    pergunta5 = "Erro ao gerar"
    print(f"✗ Erro: {e}\n")

perguntas_lista = [p for p in [pergunta1, pergunta2, pergunta3, pergunta4, pergunta5] 
                   if len(p) > 5 and "Erro" not in p]

print(f"✓ {len(perguntas_lista)} perguntas geradas com sucesso\n")

# PASSO 5: Gerar respostas
print("💬 Passo 5: Gerando respostas para as perguntas...\n")

perguntas_e_respostas = []

for i, pergunta in enumerate(perguntas_lista, 1):
    try:
        print(f"Processando pergunta {i}/{len(perguntas_lista)}...")
        print(f"  ❓ {pergunta[:70]}...")
        
        prompt_resposta = f"""{dados_formatados}

Pergunta: {pergunta}
Resposta:"""
        
        resultado_resposta = modelo_ia(prompt_resposta, max_new_tokens=150, do_sample=True,
                                       temperature=0.7, top_p=0.9, truncation=True)
        
        resposta = resultado_resposta[0]['generated_text'].split("Resposta:")[-1].strip().split('\n')[0]
        
        if len(resposta) > 10:
            print(f"  ✓ {resposta[:70]}...\n")
            perguntas_e_respostas.append({
                "numero": i,
                "pergunta": pergunta,
                "resposta": resposta,
                "status": "✓ Sucesso"
            })
        else:
            print(f"  ⚠ Resposta muito curta\n")
            perguntas_e_respostas.append({
                "numero": i,
                "pergunta": pergunta,
                "resposta": resposta,
                "status": "⚠ Resposta incompleta"
            })
        
    except Exception as e:
        print(f"  ✗ Erro: {str(e)[:60]}\n")
        perguntas_e_respostas.append({
            "numero": i,
            "pergunta": pergunta,
            "resposta": f"Erro: {str(e)[:100]}",
            "status": "✗ Falha"
        })

# PASSO 6: Armazenar no MongoDB
print("💾 Passo 6: Armazenando resultados no MongoDB...\n")

resultado_completo = {
    "tipo": "geracao_e_resposta_perguntas_opt",
    "data": datetime.now().isoformat(),
    "modelo": "facebook/opt-iml-1.3b",
    "total_funcionarios": len(funcionarios),
    "contexto": dados_formatados,
    "perguntas_e_respostas": perguntas_e_respostas,
    "total_perguntas": len(perguntas_e_respostas),
    "perguntas_bem_sucedidas": sum(1 for r in perguntas_e_respostas if r['status'] == "✓ Sucesso")
}

collection_resultados.insert_one(resultado_completo)
print("✓ Resultados armazenados com sucesso no MongoDB\n")

# PASSO 7: Relatório final
print("="*80)
print("RELATÓRIO FINAL - GERAÇÃO E RESPOSTA DE PERGUNTAS")
print("="*80)

print(f"\n📊 Estatísticas:")
print(f"  - Modelo: facebook/opt-iml-1.3b")
print(f"  - Funcionários analisados: {len(funcionarios)}")
print(f"  - Total de perguntas: {len(perguntas_e_respostas)}")
print(f"  - Bem-sucedidas: {resultado_completo['perguntas_bem_sucedidas']}")

print(f"\n❓ PERGUNTAS GERADAS E RESPONDIDAS:\n")
for item in perguntas_e_respostas:
    print(f"{'='*80}")
    print(f"Pergunta {item['numero']}:")
    print(f"  ❓ {item['pergunta']}")
    print(f"  ✓ {item['resposta']}")
    print(f"  Status: {item['status']}")
    print()

print("="*80)
print("✓ PROCESSO CONCLUÍDO!")
print("="*80)
print("\nResultados armazenados em: startup → resultados_ia")