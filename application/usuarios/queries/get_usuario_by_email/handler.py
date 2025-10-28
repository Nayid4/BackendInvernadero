from mediatr import Mediator
from infrastructure.firebase.firebase_repository import FirebaseUsuarioRepository

@Mediator.handler
class GetUsuarioByEmailHandler:
    def handle(self, request):
        repo = FirebaseUsuarioRepository()
        usuario = repo.obtener_usuario_por_correo(request.correo)
        if usuario:
            return {
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "telefono": usuario.telefono,
                "correo": usuario.correo
            }
        return None
