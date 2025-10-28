from mediatr import Mediator
from infrastructure.firebase.firebase_repository import FirebaseUsuarioRepository
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
import os

@Mediator.handler
class LoginUsuarioHandler:
    def handle(self, request):
        repo = FirebaseUsuarioRepository()
        usuario = repo.obtener_usuario_por_correo(request.correo)
        if usuario and check_password_hash(usuario.contrasena_hash, request.contrasena):
            access_token = create_access_token(identity=usuario.correo)
            return {"access_token": access_token}
        raise Exception("Credenciales inválidas")
