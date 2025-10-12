from flask import Flask

app = Flask(__name__)

@app.route('/')
def mensagem():
    return 'Oi professor! Esta é minha aplicação Python rodando no Docker!'

if __name__ == '__main.main__':
    app.run(debug=True, host='0.0.0.0', port=5000)