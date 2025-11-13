from mediatr import Mediator
from application.usuarios.commands.update_usuario.dto import UpdateUsuarioDTO
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
class UpdateUsuarioHandler:
    def handle(self, request: UpdateUsuarioDTO):
        repo = UsuarioRepository()
        usuario = repo.obtener_usuario_por_id(request.id)
        if not usuario:
            raise Exception("Usuario no encontrado")
        if request.correo:
            otro = repo.obtener_usuario_por_correo(request.correo)
            if otro and otro.id != request.id:
                raise Exception("Ya existe un usuario con el correo ingresado.")
            usuario.correo = request.correo
        if request.nombre: usuario.nombre = request.nombre
        if request.apellido: usuario.apellido = request.apellido
        if request.telefono: usuario.telefono = request.telefono
        if request.rol: usuario.rol = request.rol
        repo.guardar_usuario(usuario)
        return {"success": True}
