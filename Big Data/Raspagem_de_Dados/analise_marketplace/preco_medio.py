#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from collections import Counter

# Carrega o arquivo JSON
file_path = r'C:\Users\aluno\Desktop\wiuwiuwiu\dataset_facebook-groups-scraper_2025-11-10_23-07-12-863 (1).json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ Dados carregados: {len(data)} posts encontrados\n")
except Exception as e:
    print(f"Erro ao carregar arquivo: {e}")
    exit()

# Lista para armazenar preços encontrados
precos = []

# Padrão regex para encontrar preços (R$ 100,00 ou R$ 100.50 ou 100 reais)
padrao_preco = r'R\$\s*([\d.,]+)|(\d+)\s*reais?'

# Procura por preços em cada post
for idx, post in enumerate(data):
    texto = post.get('text', '')
    
    # Procura por padrões de preço no texto
    matches = re.finditer(padrao_preco, texto, re.IGNORECASE)
    
    for match in matches:
        valor_str = match.group(1) or match.group(2)
        if valor_str:
            # Trata diferentes formatos de número (. e , como separador)
            valor_limpo = valor_str.replace('.', '').replace(',', '.')
            try:
                preco = float(valor_limpo)
                if preco > 0:  # Valida se é um preço positivo
                    precos.append(preco)
            except:
                pass

# Calcula estatísticas
if precos:
    preco_medio = sum(precos) / len(precos)
    preco_minimo = min(precos)
    preco_maximo = max(precos)
    
    print("=" * 50)
    print("ANÁLISE DE PREÇOS DOS PRODUTOS")
    print("=" * 50)
    print(f"Total de preços encontrados: {len(precos)}")
    print(f"Preço médio: R$ {preco_medio:.2f}")
    print(f"Preço mínimo: R$ {preco_minimo:.2f}")
    print(f"Preço máximo: R$ {preco_maximo:.2f}")
    print("=" * 50)
else:
    print("Nenhum preço encontrado nos dados.")
