from flask import Flask, request, jsonify
# Importa as classes/funções do Flask:
# - Flask: cria a aplicação web
# - request: permite acessar dados da requisição HTTP (como parâmetros da URL)
# - jsonify: retorna resposta em formato JSON

app = Flask(__name__)
# Cria a instância da aplicação Flask, que é o servidor web.

@app.route("/soma", methods=["GET"])
# Define uma rota (endpoint) chamada "/soma".
# Sempre que alguém acessar http://host:porta/soma com método GET,
# a função 'soma()' será executada.

def soma():
    try:
        a = float(request.args.get("a", 0))
        # Pega o parâmetro 'a' enviado na URL (ex: /soma?a=10).
        # Se não existir, usa o valor padrão 0.
        # Converte o valor para float (número decimal).

        b = float(request.args.get("b", 0))
        # Pega o parâmetro 'b' enviado na URL (ex: /soma?b=20).
        # Se não existir, usa o valor padrão 0.
        # Também converte para float.

        return jsonify({"resultado": a + b})
        # Retorna um JSON com o resultado da soma de 'a' + 'b'.
        # Exemplo: {"resultado": 30.0}

    except Exception as e:
        # Se acontecer algum erro (ex: usuário passar texto em vez de número),
        # entra aqui no bloco de exceção.

        return jsonify({"erro": str(e)}), 400
        # Retorna um JSON com a descrição do erro e código HTTP 400 (Bad Request).

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # Esse bloco só roda se o script for executado diretamente (python app.py).
    # - host="0.0.0.0": permite que a aplicação seja acessada de fora do container.
    # - port=5000: define a porta onde o Flask vai escutar.
