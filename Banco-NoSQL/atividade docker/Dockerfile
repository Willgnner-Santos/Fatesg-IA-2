# Usa uma imagem base oficial do Python para o nosso projeto.
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Copia os arquivos de requisitos e os instala.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação.
COPY app.py .

# Expõe a porta 5000.
EXPOSE 5000

# Comando para iniciar a aplicação usando Gunicorn, com a aplicação 'app:app'
# que significa 'o objeto app que está dentro do arquivo app.py'.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]