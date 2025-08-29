from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/docker", methods=["GET"])
def flame():
    # Retorna uma resposta simples em formato JSON
    return jsonify({"message": "Subi o Docker! This is Eduardo Lucenaa!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
