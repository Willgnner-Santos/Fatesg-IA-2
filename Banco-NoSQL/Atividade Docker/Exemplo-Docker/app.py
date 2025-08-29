from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/dock", methods=["GET"])
def flame():
    return jsonify({"message": "Chama no Docker!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)