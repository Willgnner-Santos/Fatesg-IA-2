# 🧠 CogniKids - Sistema Educacional Infantil Inteligente

## 📖 Descrição

CogniKids é um aplicativo educacional interativo desenvolvido em Python com Streamlit, projetado para crianças de 7 a 9 anos. O sistema oferece atividades educativas em diferentes áreas do conhecimento, com acompanhamento de desempenho e relatórios personalizados.

## ✨ Funcionalidades

### 🔐 Sistema de Login
- Autenticação de usuários
- Perfis personalizados com avatar
- Gerenciamento de preferências

### 📊 Painel de Desempenho
- Visualização de métricas em tempo real
- Gráficos interativos de evolução
- Análise de consistência
- Identificação de áreas fortes e fracas

### 🎮 Atividades Educativas
- **Matemática**: Operações básicas e sequências
- **Português**: Ortografia, gramática e rimas
- **Lógica**: Raciocínio e resolução de problemas
- **Memória**: Exercícios de memorização
- **Ciências**: Conhecimentos gerais sobre natureza

### 📋 Relatórios e Recomendações
- Análise detalhada por tema
- Recomendações personalizadas
- Mapa de habilidades visual
- Sugestões de melhoria

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Backend CogniKids rodando (opcional, mas recomendado)

### Instalação

1. Instale as dependências:
```bash
pip install streamlit pandas matplotlib requests
```

### Execução

#### Opção 1: Com Backend (Recomendado)

1. **Inicie o backend primeiro:**
```bash
cd "C:\Users\ACER\Desktop\GRADUAÇÃO I.A\2º Periodo\Pi\CogniKidsV2.0\cognikids-backend"
docker-compose up
# ou
python run.py
```

2. **Inicie o frontend:**
```bash
cd "C:\Users\ACER\Desktop\GRADUAÇÃO I.A\2º Periodo\Pi\CogniKids3.0\cognikids"
streamlit run app.py
```

O aplicativo abrirá automaticamente no navegador em `http://localhost:8501`

**Indicadores:**
- 🟢 **API Conectada**: Usando backend Flask + MongoDB
- 🟡 **Modo Offline**: Usando dados locais simulados

#### Opção 2: Apenas Frontend (Modo Local)

Execute direto sem o backend. O sistema usará dados simulados:
```bash
streamlit run app.py
```

### Verificação

Para verificar se o backend está funcionando:
```bash
curl http://localhost:5001/api/status
```

Ou acesse a documentação em: http://localhost:5001/docs

## 👥 Contas de Teste

### Backend (Banco MongoDB) - Recomendado

**Professores:**
- Email: `carlos.antunes@escola.dev` | Senha: `senha123`
- Email: `beatriz.moreira@escola.dev` | Senha: `senha123`

**Pais/Responsáveis:**
- Email: `ricardo.alves@pais.dev` | Senha: `senha123`
- Email: `mariana.costa@pais.dev` | Senha: `senha123`
- Email: `helena.mendes@pais.dev` | Senha: `senha123`

**Alunos:**
- Email: `ana.sofia@aluno.dev` | Senha: `senha123`
- Email: `bruno.costa@aluno.dev` | Senha: `senha123`
- Email: `clara.lima@aluno.dev` | Senha: `senha123`
- Email: `diogo.mendes@aluno.dev` | Senha: `senha123`

### Modo Local (Fallback)

**Alunos (dados simulados):**
- Usuário: `maria` | Senha: `123`
- Usuário: `joao` | Senha: `456`
- Usuário: `ana` | Senha: `789`

## 📁 Estrutura do Projeto

```
cognikids/
│
├── app.py                  # Arquivo principal do Streamlit
│
├── modules/
│   ├── login.py           # Módulo de autenticação
│   ├── dashboard.py       # Painel de desempenho
│   ├── activities.py      # Atividades educativas
│   ├── reports.py         # Relatórios e análises
│   └── stats.py           # Funções estatísticas
│
├── utils/
│   └── helpers.py         # Funções auxiliares
│
├── data/
│   ├── users.json         # Dados dos usuários
│   └── progress.csv       # Histórico de progresso
│
└── assets/
    ├── styles.css         # Estilos customizados
    └── icons/             # Ícones do sistema
```

## 🎨 Design

O CogniKids utiliza uma paleta de cores vibrantes e amigáveis:

- 🟣 Roxo (`#8B5CF6`)
- 🌸 Rosa (`#EC4899`)
- 🟡 Amarelo (`#FACC15`)
- 🔵 Azul (`#3B82F6`)
- 🟢 Verde (`#10B981`)

## 📊 Análises Estatísticas

O sistema calcula automaticamente:

- **Média de acertos**: Percentual geral de respostas corretas
- **Tempo médio**: Tempo gasto em cada atividade
- **Desvio padrão**: Variação de desempenho
- **Consistência**: Estabilidade nos resultados
- **Evolução percentual**: Progresso ao longo do tempo

## 🔄 Próximos Passos

- [ ] Integração com backend real (API)
- [ ] Sistema de conquistas e badges
- [ ] Modo multijogador
- [ ] Relatórios para pais/professores
- [ ] Mais temas e atividades
- [ ] Gamificação avançada
- [ ] Suporte a múltiplos idiomas

## 📝 Licença

Projeto educacional desenvolvido para fins acadêmicos.

## 👨‍💻 Desenvolvimento

Desenvolvido com ❤️ usando:
- Python 3.x
- Streamlit
- Pandas
- Matplotlib

---

**CogniKids** - Aprendendo com diversão! 🧠✨
