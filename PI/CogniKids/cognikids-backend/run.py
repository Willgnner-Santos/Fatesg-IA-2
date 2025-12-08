from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Obtem a porta a partir das variaveis de ambiente ou utiliza 5001 como padrao
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)