from dotenv import load_dotenv
load_dotenv()

import mediator_handlers_init

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_problem_details import configure_app
from app.controllers.usuario_controller import usuario_bp
from app.controllers.planta_controller import planta_bp
from app.controllers.abanico_controller import abanico_bp
import os
import datetime

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)

jwt = JWTManager(app)
configure_app(app)  # Esto registra el middleware para ProblemDetails RFC 7807

app.register_blueprint(usuario_bp, url_prefix='/users')
app.register_blueprint(planta_bp, url_prefix='/plantas')
app.register_blueprint(abanico_bp, url_prefix='/abanico')

if __name__ == "__main__":
    app.run(debug=True)
