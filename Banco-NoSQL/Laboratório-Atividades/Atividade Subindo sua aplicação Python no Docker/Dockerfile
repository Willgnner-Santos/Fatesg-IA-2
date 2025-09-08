# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expõe a porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]