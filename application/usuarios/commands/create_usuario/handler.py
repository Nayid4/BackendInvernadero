from mediatr import Mediator
from werkzeug.security import generate_password_hash
from infrastructure.firebase.firebase_repository import FirebaseUsuarioRepository
from domain.usuario import Usuario

@Mediator.handler
class CreateUsuarioHandler:
    def handle(self, request):
        repo = FirebaseUsuarioRepository()
        usuario = Usuario(
            nombre=request.nombre,
            apellido=request.apellido,
            telefono=request.telefono,
            correo=request.correo,
            contrasena_hash=generate_password_hash(request.contrasena)
        )
        repo.guardar_usuario(usuario)
        return {"success": True, "correo": usuario.correo}
