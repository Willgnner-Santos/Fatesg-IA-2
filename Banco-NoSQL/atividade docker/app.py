from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Olá! Esta aplicação Flask está rodando dentro de um container Docker."