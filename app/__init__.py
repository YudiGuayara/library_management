# app/__init__.py

from flask import Flask
from .extensions import mongo
from .controllers import bp as library_bp

def create_app():
    app = Flask(__name__)

    # Configuración de Flask-PyMongo
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/library_management'
    mongo.init_app(app)

    # Registrar blueprint de los controladores
    app.register_blueprint(library_bp, url_prefix='/api')

    return app
