from mediatr import Mediator
from infrastructure.repositories.usuario_repository import UsuarioRepository
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

@Mediator.handler
class LoginUsuarioHandler:
    def handle(self, request):
        repo = UsuarioRepository()
        usuario = repo.obtener_usuario_por_correo(request.correo)
        if not usuario:
            raise Exception("Usuario o contraseña incorrectos")
        if not check_password_hash(usuario.contrasena_hash, request.contrasena):
            raise Exception("Usuario o contraseña incorrectos")
        access_token = create_access_token(identity=usuario.id)
        return {
            "access_token": access_token,
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "rol": usuario.rol,
                "correo": usuario.correo
            }
        }
