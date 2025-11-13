from mediatr import Mediator
from application.usuarios.commands.create_usuario.dto import CreateUsuarioDTO
from domain.usuario import Usuario
from infrastructure.repositories.usuario_repository import UsuarioRepository
from werkzeug.security import generate_password_hash
import uuid

@Mediator.handler
class CreateUsuarioHandler:
    def handle(self, request: CreateUsuarioDTO):
        repo = UsuarioRepository()
        existente = repo.obtener_usuario_por_correo(request.correo)
        if existente:
            raise Exception("Ya existe un usuario registrado con este correo.")
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
        repo.guardar_usuario(usuario)
        return {"id": usuario_id}
