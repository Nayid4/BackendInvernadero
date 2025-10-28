from mediatr import Mediator
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
class GetUsuarioByIdHandler:
    def handle(self, request):
        repo = UsuarioRepository()
        usuario = repo.obtener_usuario_por_id(request.id)
        if usuario:
            return {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "telefono": usuario.telefono,
                "rol": usuario.rol,
                "correo": usuario.correo
            }
        return None
