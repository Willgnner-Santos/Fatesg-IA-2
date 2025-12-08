import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import random

# --- 1. Definição com SOBREPOSIÇÃO INTENSA (Para baixar acurácia) ---
ESTADOS = {
    'CALMO': {
        'bpm_range': (55, 100), 
        'gsr_range': (0.1, 1.0), 
        'movement_range': (0.1, 1.4), 
        'crise_target': 0
    },
    
    # ATIVO: Aumentamos o GSR (suor) para confundir muito com TENSO
    'ATIVO': {
        'bpm_range': (85, 165), # Faixa muito ampla
        'gsr_range': (0.4, 3.0), # Suor alto (confunde com Ansiedade)
        'movement_range': (0.5, 4.5), # Às vezes para para descansar (confunde)
        'crise_target': 0
    },
    
    # TENSO: Diminuímos o limiar de movimento para confundir com CALMO/ATIVO
    'TENSO': {
        'bpm_range': (90, 160), # Quase idêntico ao ATIVO
        'gsr_range': (1.0, 3.8), 
        'movement_range': (0.0, 2.0), # Agitação leve (confunde com ATIVO leve)
        'crise_target': 1
    },
    
    # CRISE: Mantemos extremo, mas com margem para erro
    'CRISE': {
        'bpm_range': (120, 190), 
        'gsr_range': (2.2, 6.5), 
        'movement_range': (0.0, 3.5), # Totalmente imprevisível
        'crise_target': 1
    }
}

# Personas (Mantidas)
PERSONAS = {
    'ANA_CALMA': {'CALMO': [0.8, 0.1, 0.1, 0.0], 'ATIVO': [0.6, 0.3, 0.1, 0.0], 'TENSO': [0.4, 0.1, 0.5, 0.0], 'CRISE': [0.5, 0.1, 0.4, 0.0]},
    'HEITOR_ANSIOSO': {'CALMO': [0.5, 0.1, 0.4, 0.0], 'ATIVO': [0.4, 0.2, 0.4, 0.0], 'TENSO': [0.1, 0.1, 0.7, 0.1], 'CRISE': [0.0, 0.1, 0.6, 0.3]},
    'CLARA_NORMAL': {'CALMO': [0.7, 0.2, 0.1, 0.0], 'ATIVO': [0.6, 0.3, 0.1, 0.0], 'TENSO': [0.3, 0.2, 0.5, 0.0], 'CRISE': [0.2, 0.2, 0.5, 0.1]},
    'DIOGO_MODERADO': {'CALMO': [0.6, 0.2, 0.2, 0.0], 'ATIVO': [0.5, 0.3, 0.2, 0.0], 'TENSO': [0.2, 0.2, 0.5, 0.1], 'CRISE': [0.1, 0.2, 0.5, 0.2]}
}

def gerar_dados_por_estado(estado):
    config = ESTADOS[estado]
    bpm = np.random.randint(config['bpm_range'][0], config['bpm_range'][1])
    gsr = np.random.uniform(config['gsr_range'][0], config['gsr_range'][1])
    movement = np.random.uniform(config['movement_range'][0], config['movement_range'][1])
    
    # --- RUÍDO AUMENTADO PARA 25% (Caos total) ---
    noise = 0.25 
    bpm += np.random.normal(0, bpm * noise)
    gsr += np.random.normal(0, gsr * noise)
    movement += np.random.normal(0, movement * noise)
    
    # --- ROTULAGEM ERRADA (8%) ---
    # Simula o professor que não viu a crise ou marcou crise sem querer
    target = config['crise_target']
    if random.random() < 0.08: 
        target = 1 - target

    return {'bpm': bpm, 'gsr': gsr, 'movement_score': movement, 'crise': target}

def proximo_estado(atual, persona_config):
    return random.choices(['CALMO', 'ATIVO', 'TENSO', 'CRISE'], weights=persona_config[atual], k=1)[0]

# --- Geração ---
data = []
print("Gerando dados com ALTO NIVEL DE REALISMO (Ruido 25%)...")
for persona, config in PERSONAS.items():
    estado = 'CALMO'
    for _ in range(3000): 
        d = gerar_dados_por_estado(estado)
        data.append(d)
        estado = proximo_estado(estado, config)

df = pd.DataFrame(data)

# --- Treinamento ---
X = df[['bpm', 'gsr', 'movement_score']]
y = df['crise']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("\nTreinando Modelo 'Limitado' (Mais Realista)...")
# Reduzimos max_depth para 6 para impedir que ele 'decore' os dados
model = RandomForestClassifier(n_estimators=100, max_depth=6, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# --- Avaliação ---
y_pred = model.predict(X_test)
print("\nRelatorio de Performance (Meta: ~75-82%):")
print(classification_report(y_test, y_pred))

print("\nMatriz de Confusao:")
print(confusion_matrix(y_test, y_pred))

joblib.dump(model, "model.joblib")
print("\nOK: Modelo salvo como 'model.joblib'!")