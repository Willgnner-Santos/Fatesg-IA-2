#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Configurar estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

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
precos_com_outliers = []

# Padrão regex para encontrar preços
padrao_preco = r'R\$\s*([\d.,]+)|(\d+)\s*reais?'

# Procura por preços em cada post
for idx, post in enumerate(data):
    texto = post.get('text', '')
    
    # Procura por padrões de preço no texto
    matches = re.finditer(padrao_preco, texto, re.IGNORECASE)
    
    for match in matches:
        valor_str = match.group(1) or match.group(2)
        if valor_str:
            # Trata diferentes formatos de número
            valor_limpo = valor_str.replace('.', '').replace(',', '.')
            try:
                preco = float(valor_limpo)
                if preco > 0:
                    precos_com_outliers.append(preco)
                    # Filtra outliers (preços razoáveis para produtos)
                    if preco < 100000:  # Limite para produtos normais
                        precos.append(preco)
            except:
                pass

print(f"Preços encontrados (sem filtro): {len(precos_com_outliers)}")
print(f"Preços válidos (com filtro): {len(precos)}\n")

if precos:
    # Criar figura com múltiplos subplots
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Histograma de distribuição de preços
    ax1 = plt.subplot(2, 3, 1)
    plt.hist(precos, bins=15, color='#2ecc71', edgecolor='black', alpha=0.7)
    plt.title('Distribuição de Preços', fontsize=12, fontweight='bold')
    plt.xlabel('Preço (R$)')
    plt.ylabel('Frequência')
    plt.grid(axis='y', alpha=0.3)
    
    # 2. Boxplot para detectar outliers
    ax2 = plt.subplot(2, 3, 2)
    plt.boxplot(precos, vert=True, patch_artist=True, 
                boxprops=dict(facecolor='#3498db', alpha=0.7),
                medianprops=dict(color='red', linewidth=2))
    plt.title('Boxplot dos Preços', fontsize=12, fontweight='bold')
    plt.ylabel('Preço (R$)')
    plt.grid(axis='y', alpha=0.3)
    
    # 3. Estatísticas em texto
    ax3 = plt.subplot(2, 3, 3)
    ax3.axis('off')
    
    preco_medio = sum(precos) / len(precos)
    preco_minimo = min(precos)
    preco_maximo = max(precos)
    preco_mediana = sorted(precos)[len(precos)//2]
    
    stats_text = f"""
    ESTATÍSTICAS DE PREÇOS
    {'='*40}
    
    Total de preços: {len(precos)}
    Preço médio: R$ {preco_medio:,.2f}
    Preço mediana: R$ {preco_mediana:,.2f}
    Preço mínimo: R$ {preco_minimo:,.2f}
    Preço máximo: R$ {preco_maximo:,.2f}
    
    Desvio padrão: R$ {(sum((x-preco_medio)**2 for x in precos)/len(precos))**0.5:,.2f}
    """
    
    ax3.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
            verticalalignment='center', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5))
    
    # 4. Gráfico de dispersão
    ax4 = plt.subplot(2, 3, 4)
    plt.scatter(range(len(precos)), sorted(precos), alpha=0.6, s=100, color='#e74c3c')
    plt.title('Preços Ordenados', fontsize=12, fontweight='bold')
    plt.xlabel('Índice do Produto')
    plt.ylabel('Preço (R$)')
    plt.grid(alpha=0.3)
    
    # 5. Faixa de preços
    ax5 = plt.subplot(2, 3, 5)
    faixas = ['R$0-100', 'R$100-500', 'R$500-1000', 'R$1000-5000', 'R$5000+']
    contagem_faixas = [
        len([p for p in precos if 0 <= p < 100]),
        len([p for p in precos if 100 <= p < 500]),
        len([p for p in precos if 500 <= p < 1000]),
        len([p for p in precos if 1000 <= p < 5000]),
        len([p for p in precos if p >= 5000])
    ]
    
    cores = ['#9b59b6', '#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    bars = plt.bar(faixas, contagem_faixas, color=cores, alpha=0.7, edgecolor='black')
    plt.title('Produtos por Faixa de Preço', fontsize=12, fontweight='bold')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45, ha='right')
    
    # Adicionar valores nas barras
    for bar, count in zip(bars, contagem_faixas):
        if count > 0:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(count), ha='center', va='bottom', fontweight='bold')
    
    # 6. Comparação com outliers
    ax6 = plt.subplot(2, 3, 6)
    dados_comparacao = [precos, precos_com_outliers]
    labels_comparacao = [f'Sem Outliers\n({len(precos)} itens)', 
                         f'Com Outliers\n({len(precos_com_outliers)} itens)']
    
    bp = plt.boxplot(dados_comparacao, labels=labels_comparacao, patch_artist=True,
                     boxprops=dict(facecolor='#1abc9c', alpha=0.7))
    plt.title('Comparação: Com vs Sem Outliers', fontsize=12, fontweight='bold')
    plt.ylabel('Preço (R$)')
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\aluno\Desktop\wiuwiuwiu\analise_marketplace\graficos_precos.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Gráficos salvos em: graficos_precos.png")
    
    plt.show()
    
else:
    print("Nenhum preço encontrado para gerar gráficos.")
