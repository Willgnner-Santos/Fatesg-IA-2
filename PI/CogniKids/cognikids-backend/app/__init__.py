import os
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Objetos globais para extensões Flask
mongo = PyMongo()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    
    # Configuracoes de timeout e pool de conexoes do MongoDB
    app.config["MONGO_CONNECT_TIMEOUT_MS"] = 5000
    app.config["MONGO_SERVER_SELECTION_TIMEOUT_MS"] = 5000
    app.config["MONGO_SOCKET_TIMEOUT_MS"] = 10000
    app.config["MONGO_MAX_POOL_SIZE"] = 50
    app.config["MONGO_MIN_POOL_SIZE"] = 10

    # Inicializar extensoes Flask
    mongo.init_app(app)
    bcrypt.init_app(app)

    # Registro dos Blueprints
    # Autenticacao
    from .Controllers.auth_controller import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    print("Blueprint de autenticacao registrado com sucesso")
    
    # IoT
    from .Controllers.iot_controller import iot_bp
    app.register_blueprint(iot_bp, url_prefix='/api/iot')
    print("Blueprint de IoT registrado com sucesso")
    
    # Estudantes
    from .Controllers.student_controller import student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/api/students')
    print("Blueprint de estudantes registrado com sucesso")
    
    # Professores
    from .Controllers.teacher_controller import teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix='/api/teachers')
    print("Blueprint de professores registrado com sucesso")
    
    # Responsaveis
    from .Controllers.parent_controller import parent_blueprint
    app.register_blueprint(parent_blueprint, url_prefix='/api/parents')
    print("Blueprint de responsaveis registrado com sucesso")
    
    # Turmas
    from .Controllers.class_controller import class_blueprint
    app.register_blueprint(class_blueprint, url_prefix='/api/classes')
    print("Blueprint de turmas registrado com sucesso")
    
    # Notas
    from .Controllers.grade_controller import grade_blueprint
    app.register_blueprint(grade_blueprint, url_prefix='/api/grades')
    print("Blueprint de notas registrado com sucesso")
    
    # Desafios  
    from .Controllers.challenge_controller import challenge_blueprint
    app.register_blueprint(challenge_blueprint, url_prefix='/api/challenges')
    print("Blueprint de desafios registrado com sucesso")

    @app.route('/')
    def index():
        return "Servidor CogniKids no ar! API disponível em /api"

    @app.route('/status')
    def status():
        return jsonify({"status": "sucesso", "message": "Servidor funcionando corretamente!"})

    return app