from mediatr import Mediator
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
class GetUsuarioByCorreoHandler:
    def handle(self, request):
        repo = UsuarioRepository()
        usuario = repo.obtener_usuario_por_correo(request.correo)
        if usuario:
            return {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "telefono": usuario.telefono,
                "rol": usuario.rol,
                "correo": usuario.correo,
            }
        return None
