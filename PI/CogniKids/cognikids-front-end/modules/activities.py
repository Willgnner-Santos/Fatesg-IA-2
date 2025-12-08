"""
Módulo de atividades educativas do CogniKids
"""

import streamlit as st
import random
import time
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import salvar_resposta

# Banco de questões por tema
QUESTOES = {
    "Matemática": [
        {
            "pergunta": "Quanto é 5 + 3?",
            "opcoes": ["6", "7", "8", "9"],
            "resposta_correta": "8",
            "dica": "Use os dedos para contar!"
        },
        {
            "pergunta": "Qual é o resultado de 10 - 4?",
            "opcoes": ["5", "6", "7", "8"],
            "resposta_correta": "6",
            "dica": "Tire 4 de 10!"
        },
        {
            "pergunta": "Quanto é 3 x 2?",
            "opcoes": ["5", "6", "7", "8"],
            "resposta_correta": "6",
            "dica": "É como somar 3 + 3!"
        },
        {
            "pergunta": "Quantos são 15 dividido por 3?",
            "opcoes": ["3", "4", "5", "6"],
            "resposta_correta": "5",
            "dica": "Quantas vezes o 3 cabe no 15?"
        },
        {
            "pergunta": "Qual é o próximo número: 2, 4, 6, __?",
            "opcoes": ["7", "8", "9", "10"],
            "resposta_correta": "8",
            "dica": "Os números estão pulando de 2 em 2!"
        }
    ],
    "Português": [
        {
            "pergunta": "Quantas vogais tem a palavra CASA?",
            "opcoes": ["1", "2", "3", "4"],
            "resposta_correta": "2",
            "dica": "As vogais são: A, E, I, O, U"
        },
        {
            "pergunta": "Qual palavra está escrita corretamente?",
            "opcoes": ["Cajxa", "Caixa", "Kaisha", "Cayxa"],
            "resposta_correta": "Caixa",
            "dica": "Pense no som das letras!"
        },
        {
            "pergunta": "Complete: O gato _____ no telhado.",
            "opcoes": ["está", "estão", "estar", "estamos"],
            "resposta_correta": "está",
            "dica": "O gato é só um, singular!"
        },
        {
            "pergunta": "Qual é o plural de 'flor'?",
            "opcoes": ["flores", "flors", "florais", "floreses"],
            "resposta_correta": "flores",
            "dica": "Adicione ES no final!"
        },
        {
            "pergunta": "Qual palavra rima com 'gato'?",
            "opcoes": ["rato", "casa", "bola", "carro"],
            "resposta_correta": "rato",
            "dica": "Procure palavras que terminam com o mesmo som!"
        }
    ],
    "Lógica": [
        {
            "pergunta": "Se todos os pássaros voam e o pardal é um pássaro, então...",
            "opcoes": ["O pardal nada", "O pardal voa", "O pardal corre", "O pardal pula"],
            "resposta_correta": "O pardal voa",
            "dica": "Se todos os pássaros voam..."
        },
        {
            "pergunta": "Complete a sequência: 🔴 🔵 🔴 🔵 __",
            "opcoes": ["🔴", "🔵", "🟢", "🟡"],
            "resposta_correta": "🔴",
            "dica": "Observe o padrão que se repete!"
        },
        {
            "pergunta": "João tem 3 maçãs. Maria tem o dobro. Quantas maçãs Maria tem?",
            "opcoes": ["3", "5", "6", "9"],
            "resposta_correta": "6",
            "dica": "Dobro é multiplicar por 2!"
        },
        {
            "pergunta": "Qual forma não pertence ao grupo: 🔺 🔲 ⭕ 🔺",
            "opcoes": ["🔺", "🔲", "⭕", "Todas pertencem"],
            "resposta_correta": "🔲",
            "dica": "Procure qual é diferente das outras!"
        },
        {
            "pergunta": "Se ontem foi terça, que dia é amanhã?",
            "opcoes": ["Segunda", "Terça", "Quarta", "Quinta"],
            "resposta_correta": "Quinta",
            "dica": "Ontem = terça, hoje = quarta, amanhã = ?"
        }
    ],
    "Memória": [
        {
            "pergunta": "Olhe bem: 🍎 🍌 🍊. Qual fruta estava no meio?",
            "opcoes": ["🍎 Maçã", "🍌 Banana", "🍊 Laranja", "🍇 Uva"],
            "resposta_correta": "🍌 Banana",
            "dica": "A fruta do meio estava entre a maçã e a laranja!"
        },
        {
            "pergunta": "Memorize: GATO - CACHORRO - PEIXE. Qual era o primeiro?",
            "opcoes": ["GATO", "CACHORRO", "PEIXE", "PÁSSARO"],
            "resposta_correta": "GATO",
            "dica": "Era um animal que faz miau!"
        },
        {
            "pergunta": "Sequência: 5, 8, 11. Qual é o próximo número?",
            "opcoes": ["12", "13", "14", "15"],
            "resposta_correta": "14",
            "dica": "Está aumentando de 3 em 3!"
        },
        {
            "pergunta": "Cores mostradas: 🔴 🟢 🔵. Qual cor NÃO foi mostrada?",
            "opcoes": ["🔴 Vermelho", "🟡 Amarelo", "🟢 Verde", "🔵 Azul"],
            "resposta_correta": "🟡 Amarelo",
            "dica": "Procure uma cor que não estava lá!"
        },
        {
            "pergunta": "Número secreto: 42. Qual era o número?",
            "opcoes": ["24", "42", "44", "52"],
            "resposta_correta": "42",
            "dica": "Estava escrito logo acima!"
        }
    ],
    "Ciências": [
        {
            "pergunta": "Quantas patas tem um cachorro?",
            "opcoes": ["2", "4", "6", "8"],
            "resposta_correta": "4",
            "dica": "Conte as pernas do cachorro!"
        },
        {
            "pergunta": "O que as plantas precisam para crescer?",
            "opcoes": ["Água e sol", "Só água", "Só sol", "Nada"],
            "resposta_correta": "Água e sol",
            "dica": "Plantas precisam de mais de uma coisa!"
        },
        {
            "pergunta": "Qual animal voa?",
            "opcoes": ["Peixe", "Cachorro", "Pássaro", "Gato"],
            "resposta_correta": "Pássaro",
            "dica": "Tem asas e penas!"
        },
        {
            "pergunta": "Quantos dias tem uma semana?",
            "opcoes": ["5", "6", "7", "8"],
            "resposta_correta": "7",
            "dica": "Segunda até domingo!"
        },
        {
            "pergunta": "O que acontece com a água quando congela?",
            "opcoes": ["Vira gelo", "Vira vapor", "Desaparece", "Fica quente"],
            "resposta_correta": "Vira gelo",
            "dica": "Fica muito frio e duro!"
        }
    ]
}

def inicializar_atividade():
    """
    Inicializa as variáveis de sessão da atividade
    """
    if 'atividade_iniciada' not in st.session_state:
        st.session_state['atividade_iniciada'] = False
    if 'questoes_atuais' not in st.session_state:
        st.session_state['questoes_atuais'] = []
    if 'questao_index' not in st.session_state:
        st.session_state['questao_index'] = 0
    if 'acertos' not in st.session_state:
        st.session_state['acertos'] = 0
    if 'tempo_inicio' not in st.session_state:
        st.session_state['tempo_inicio'] = None
    if 'respostas_usuario' not in st.session_state:
        st.session_state['respostas_usuario'] = []

def mostrar_atividades(usuario):
    """
    Mostra a interface de atividades educativas
    
    Args:
        usuario (dict): Dados do usuário logado
    """
    st.markdown("## Atividades Educativas")
    st.write("")
    
    inicializar_atividade()
    
    # Se não iniciou atividade, mostra seleção de tema
    if not st.session_state['atividade_iniciada']:
        mostrar_selecao_tema()
    else:
        # Mostra a questão atual
        mostrar_questao_atual(usuario)

def mostrar_selecao_tema():
    """
    Mostra a tela de seleção de tema
    """
    st.markdown("### Escolha um tema para praticar:")
    st.write("")
    
    # Cria cards para cada tema
    cols = st.columns(3)
    
    temas_info = {
        "Matemática": {"emoji": "🔢", "cor": "#8B5CF6", "desc": "Números e contas"},
        "Português": {"emoji": "📝", "cor": "#EC4899", "desc": "Palavras e letras"},
        "Lógica": {"emoji": "🧩", "cor": "#3B82F6", "desc": "Raciocínio e padrões"},
        "Memória": {"emoji": "🧠", "cor": "#FACC15", "desc": "Lembre-se bem!"},
        "Ciências": {"emoji": "🔬", "cor": "#10B981", "desc": "Natureza e mundo"}
    }
    
    temas = list(QUESTOES.keys())
    
    for i, tema in enumerate(temas):
        col = cols[i % 3]
        info = temas_info.get(tema, {"emoji": "📖", "cor": "#6B7280", "desc": "Aprenda mais"})
        
        with col:
            st.markdown(f"""
                <div style='padding: 1.5rem; background: {info['cor']}; border-radius: 15px; 
                text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
                    <h2 style='margin: 0; font-size: 3rem;'>{info['emoji']}</h2>
                    <h3 style='margin: 0.5rem 0;'>{tema}</h3>
                    <p style='margin: 0; opacity: 0.9;'>{info['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Começar {tema}", key=f"btn_{tema}", width="stretch"):
                iniciar_atividade(tema)
                st.rerun()

def iniciar_atividade(tema):
    """
    Inicia uma atividade do tema escolhido
    
    Args:
        tema (str): Tema escolhido
    """
    # Seleciona questões do tema
    questoes = QUESTOES[tema].copy()
    random.shuffle(questoes)
    
    # Inicializa variáveis de sessão
    st.session_state['atividade_iniciada'] = True
    st.session_state['tema_atual'] = tema
    st.session_state['questoes_atuais'] = questoes
    st.session_state['questao_index'] = 0
    st.session_state['acertos'] = 0
    st.session_state['tempo_inicio'] = time.time()
    st.session_state['respostas_usuario'] = []
    st.session_state['mostrar_feedback'] = False

def mostrar_questao_atual(usuario):
    """
    Mostra a questão atual
    
    Args:
        usuario (dict): Dados do usuário logado
    """
    questoes = st.session_state['questoes_atuais']
    index = st.session_state['questao_index']
    tema = st.session_state['tema_atual']
    
    # Se terminou todas as questões
    if index >= len(questoes):
        mostrar_resultado_final(usuario)
        return
    
    questao = questoes[index]
    
    # Barra de progresso
    progresso = (index / len(questoes)) * 100
    st.markdown(f"""
        <div style='background: #E5E7EB; border-radius: 10px; height: 20px; margin-bottom: 1rem;'>
            <div style='background: linear-gradient(90deg, #8B5CF6, #EC4899); 
            width: {progresso}%; height: 100%; border-radius: 10px; 
            transition: width 0.3s;'></div>
        </div>
        <p style='text-align: center; color: #6B7280;'>
            Questão {index + 1} de {len(questoes)}
        </p>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Card da questão
    st.markdown(f"""
        <div style='padding: 2rem; background: white; border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #8B5CF6;'>
            <h2 style='color: #8B5CF6; margin-bottom: 1rem;'>{tema}</h2>
            <h3 style='color: #1F2937; margin-bottom: 1.5rem;'>{questao['pergunta']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # Opções de resposta
    if 'mostrar_feedback' not in st.session_state:
        st.session_state['mostrar_feedback'] = False
    
    if not st.session_state['mostrar_feedback']:
        # Mostra as opções
        cols = st.columns(2)
        
        for i, opcao in enumerate(questao['opcoes']):
            col = cols[i % 2]
            
            with col:
                if st.button(
                    opcao,
                    key=f"opcao_{index}_{i}",
                    width="stretch",
                    type="secondary"
                ):
                    verificar_resposta(opcao, questao['resposta_correta'])
        
        # Botão de dica
        st.write("")
        with st.expander("Precisa de uma dica?"):
            st.info(questao['dica'])
    else:
        # Mostra o feedback
        mostrar_feedback(questao)

def verificar_resposta(resposta_usuario, resposta_correta):
    """
    Verifica se a resposta está correta
    
    Args:
        resposta_usuario (str): Resposta escolhida pelo usuário
        resposta_correta (str): Resposta correta
    """
    if resposta_usuario == resposta_correta:
        st.session_state['acertos'] += 1
        st.session_state['ultima_resposta_correta'] = True
    else:
        st.session_state['ultima_resposta_correta'] = False
    
    st.session_state['respostas_usuario'].append({
        'resposta': resposta_usuario,
        'correta': resposta_usuario == resposta_correta
    })
    
    st.session_state['mostrar_feedback'] = True
    st.rerun()

def mostrar_feedback(questao):
    """
    Mostra feedback após resposta
    
    Args:
        questao (dict): Dados da questão
    """
    if st.session_state['ultima_resposta_correta']:
        st.success("Parabéns! Você acertou!")
        st.balloons()
    else:
        st.error(f"Ops! A resposta correta era: **{questao['resposta_correta']}**")
    
    st.write("")
    
    if st.button("Próxima Questão", type="primary", width="stretch"):
        st.session_state['questao_index'] += 1
        st.session_state['mostrar_feedback'] = False
        st.rerun()

def mostrar_resultado_final(usuario):
    """
    Mostra o resultado final da atividade
    
    Args:
        usuario (dict): Dados do usuário logado
    """
    acertos = st.session_state['acertos']
    total = len(st.session_state['questoes_atuais'])
    tempo_total = time.time() - st.session_state['tempo_inicio']
    tema = st.session_state['tema_atual']
    
    percentual = (acertos / total) * 100
    pontuacao = int(percentual)
    
    # Salva o resultado
    salvar_resposta(
        usuario_id=usuario['id'],
        tema=tema,
        acertos=acertos,
        total_questoes=total,
        tempo_resposta=round(tempo_total, 1),
        pontuacao=pontuacao
    )
    
    # Determina emoji e mensagem baseado no desempenho
    if percentual >= 90:
        emoji = "🌟"
        mensagem = "Excelente! Você é incrível!"
        cor = "#10B981"
    elif percentual >= 70:
        emoji = "😊"
        mensagem = "Muito bem! Continue assim!"
        cor = "#FACC15"
    elif percentual >= 50:
        emoji = "😐"
        mensagem = "Bom trabalho! Pratique mais!"
        cor = "#F59E0B"
    else:
        emoji = "😢"
        mensagem = "Não desista! Tente novamente!"
        cor = "#EF4444"
    
    # Card de resultado
    st.markdown(f"""
        <div style='padding: 3rem; background: {cor}; border-radius: 20px; 
        text-align: center; color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.2);'>
            <h1 style='font-size: 5rem; margin: 0;'>{emoji}</h1>
            <h2 style='margin: 1rem 0;'>{mensagem}</h2>
            <h1 style='font-size: 3rem; margin: 1rem 0;'>{acertos}/{total}</h1>
            <p style='font-size: 1.5rem; opacity: 0.9;'>{percentual:.0f}% de acertos</p>
            <p style='font-size: 1.2rem; opacity: 0.8;'>Tempo: {tempo_total:.0f}s</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Tentar Novamente", width="stretch", type="secondary"):
            iniciar_atividade(tema)
            st.rerun()
    
    with col2:
        if st.button("Escolher Outro Tema", width="stretch", type="primary"):
            st.session_state['atividade_iniciada'] = False
            st.rerun()


