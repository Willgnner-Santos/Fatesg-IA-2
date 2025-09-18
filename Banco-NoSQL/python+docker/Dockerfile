# Usa uma imagem base oficial do Python.
# O "slim" significa que é uma versão mais leve da imagem, sem ferramentas extras.
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container.
# Todos os comandos a seguir serão executados a partir deste diretório.
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho.
COPY requirements.txt .

# Instala as dependências especificadas no requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto (no caso, apenas o app.py).
COPY . .

# Expõe a porta que a aplicação vai usar. Isso é apenas documentação.
EXPOSE 5000

# Define o comando que será executado quando o container for iniciado.
# O comando python app.py é o que inicia o nosso servidor Flask.
CMD ["python", "app.py"]