from flask import Flask
from flask_jwt_extended import JWTManager
from flask_problem_details import ProblemDetails, problem_details
from werkzeug.exceptions import HTTPException
from app.controllers.usuario_controller import usuario_bp
from app.controllers.planta_controller import planta_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
ProblemDetails(app)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return problem_details(
        title=e.name,
        status=e.code,
        detail=e.description
    ), e.code

@app.errorhandler(Exception)
def handle_generic_exception(e):
    code = 500
    return problem_details(
        title="Ocurrió un error",
        status=code,
        detail=str(e)
    ), code

app.register_blueprint(usuario_bp, url_prefix='/api/users')
app.register_blueprint(planta_bp, url_prefix='/api/plantas')

if __name__ == "__main__":
    app.run(debug=True)
