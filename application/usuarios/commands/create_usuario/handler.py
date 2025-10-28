from mediatr import Mediator
from domain.usuario import Usuario
from infrastructure.repositories.usuario_repository import UsuarioRepository
from werkzeug.security import generate_password_hash
import uuid

@Mediator.handler
class CreateUsuarioHandler:
    def handle(self, request):
        usuario_id = str(uuid.uuid4())
        usuario = Usuario(
            id=usuario_id,
            nombre=request.nombre,
            apellido=request.apellido,
            telefono=request.telefono,
            rol=request.rol,
            correo=request.correo,
            contrasena_hash=generate_password_hash(request.contrasena)
        )
        repo = UsuarioRepository()
        repo.guardar_usuario(usuario)
        return {"id": usuario_id}
