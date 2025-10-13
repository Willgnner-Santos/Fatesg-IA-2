from flask import Flask
import os

app = Flask(__name__)
counter_file = "visitas.txt"

if not os.path.exists(counter_file):
    with open(counter_file, "w") as f:
        f.write("0")

@app.route('/')
def home():
    with open(counter_file, "r") as f:
        count = int(f.read())

    count += 1

    with open(counter_file, "w") as f:
        f.write(str(count))

    return f"<h1>Olá, User!</h1><p>Esta página foi visitada {count} vezes </p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
