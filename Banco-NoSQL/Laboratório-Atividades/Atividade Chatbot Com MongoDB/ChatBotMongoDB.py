# Importação das bibliotecas necessárias
import pymongo  # Biblioteca para conectar e manipular o banco de dados MongoDB
from transformers import pipeline  # Biblioteca para carregar modelos de IA da Hugging Face

# Conectar ao MongoDB
client = pymongo.MongoClient("")  
# Criamos uma conexão com o MongoDB rodando localmente na porta 27017.

db = client["chatbot"]  
# Acessamos (ou criamos, se não existir) o banco de dados chamado "chatbot".

collection = db["conversas"]  
# Acessamos (ou criamos, se não existir) a coleção "conversas", onde armazenaremos as interações com o modelo de IA.

# Criar um pipeline para geração de texto usando um modelo da Hugging Face
modelo = pipeline("text-generation", model="facebook/opt-1.3b")  
# "text-generation": Indica que estamos usando um modelo especializado na geração de texto.
# "facebook/opt-1.3b": Especifica o modelo escolhido, um modelo leve de 1.3 bilhões de parâmetros da Meta (Facebook).

# Definir a pergunta que será enviada para o modelo de IA
pergunta = "O que é MongoDB?"
pergunta = "Qual a Capital do Brasil?"

# Esta é a pergunta que será enviada para o modelo, mas pode ser alterada para outras questões.

# Gerar resposta usando o modelo de IA
resposta = modelo(pergunta, max_length=100, do_sample=True)[0]["generated_text"]  
# `max_length=100`: Define o tamanho máximo da resposta em tokens.  
# Se for muito curto, a resposta pode ser cortada; se for muito longo, pode gerar um texto irrelevante.  
# `do_sample=True`: Ativa a amostragem aleatória, permitindo que o modelo gere respostas variadas em cada execução.  
# `[0]["generated_text"]`: O modelo retorna uma lista de respostas, pegamos a primeira e extraímos apenas o texto gerado.

# Armazenar a pergunta e resposta no banco de dados MongoDB
collection.insert_one({
    "pergunta": pergunta,
    "resposta": resposta
})  
# O método `insert_one()` insere um documento JSON contendo a pergunta e a resposta gerada pelo modelo.

# Exibir mensagem de sucesso no terminal
print("Resposta armazenada com sucesso!")  
# Confirma que a interação foi salva no banco.

# Exibir a pergunta e a resposta gerada no terminal
print("Pergunta:", pergunta)  
print("Resposta:", resposta)  
# Exibe no terminal a pergunta feita e a resposta gerada pelo modelo de IA.


