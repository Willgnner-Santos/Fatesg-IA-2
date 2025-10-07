from app.main import app

# Este bloco garante que o servidor só será executado
# quando este script for chamado diretamente.
if __name__ == '__main__':
    # app.run(debug=True) inicia o servidor em modo de depuração.
    # Isso reinicia o servidor automaticamente a cada alteração no código.
    app.run(host='0.0.0.0', port=5000, debug=True)