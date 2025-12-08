import os
from dotenv import load_dotenv

# Carrega as variaveis de ambiente do arquivo .env
load_dotenv()

# Importa a funcao create_app do modulo app
from app import create_app

# Cria a instancia da aplicacao utilizando o padrao Factory
app = create_app()

if __name__ == '__main__':
    # Inicia o servidor na porta 5001 com acesso externo habilitado
    app.run(host='0.0.0.0', port=5001, debug=True)