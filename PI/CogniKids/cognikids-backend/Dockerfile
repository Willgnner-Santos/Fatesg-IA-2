# 1. Imagem Base: Começamos com uma imagem oficial do Python.
FROM python:3.9-slim

# 2. Diretório de Trabalho: Define o diretório onde nosso código ficará dentro do contêiner.
WORKDIR /app

# 3. Copiar Arquivos: Copia os arquivos de dependências primeiro.
# Isso é uma otimização: o Docker só reinstalará as dependências se este arquivo mudar.
COPY requirements.txt .

# 4. Instalar Dependências: Instala as bibliotecas Python.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o Código da Aplicação: Copia o resto dos arquivos do nosso backend.
COPY . .

# 6. Expor a Porta: Informa ao Docker que nossa aplicação Flask rodará na porta 5001.
EXPOSE 5001

# 7. Comando de Execução: O comando que será executado quando o contêiner iniciar.
CMD ["python", "run.py"]