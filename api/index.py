#from dotenv import load_dotenv
#load_dotenv()

# --- INICIO DE SOLUCIÓN DE RUTA ---
import sys
import os
# Agregamos la carpeta padre (la raíz del proyecto) a la ruta de búsqueda.
# Esto es necesario porque index.py ahora está en la carpeta 'api'.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# --- FIN DE SOLUCIÓN DE RUTA ---


# Asegúrate de que esta línea esté antes de importar los controladores
import mediator_handlers_init

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_problem_details import configure_app
from flask_cors import CORS
from app.controllers.usuario_controller import usuario_bp
from app.controllers.planta_controller import planta_bp
from app.controllers.planta_optimo_controller import planta_optimos_bp
from app.controllers.control_controller import control_bp
from app.controllers.control_planta_controller import control_planta_bp
from app.controllers.dataset_controller import csv_dataset_bp
from app.controllers.circuito_controller import circuit_bp

import os
import datetime

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=150)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=160)

jwt = JWTManager(app)
configure_app(app)  # Esto registra el middleware para ProblemDetails RFC 7807
CORS(app)  # Habilita CORS para la aplicación Flask

app.register_blueprint(usuario_bp, url_prefix='/users')
app.register_blueprint(planta_bp, url_prefix='/plantas')
app.register_blueprint(planta_optimos_bp, url_prefix='/plantas-optimos')
app.register_blueprint(control_bp, url_prefix='/control')
app.register_blueprint(control_planta_bp, url_prefix='/control-planta')
app.register_blueprint(csv_dataset_bp, url_prefix='/datasets')
app.register_blueprint(circuit_bp, url_prefix='/circuito')

if __name__ == "__main__":
    app.run(debug=True)
