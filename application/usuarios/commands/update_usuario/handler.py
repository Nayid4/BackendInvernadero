from mediatr import Mediator
from infrastructure.firebase.firebase_repository import FirebaseUsuarioRepository

@Mediator.handler
class UpdateUsuarioHandler:
    def handle(self, request):
        repo = FirebaseUsuarioRepository()
        usuario = repo.obtener_usuario_por_correo(request.correo)
        if not usuario:
            raise Exception("Usuario no encontrado")
        if request.nombre: usuario.nombre = request.nombre
        if request.apellido: usuario.apellido = request.apellido
        if request.telefono: usuario.telefono = request.telefono
        repo.guardar_usuario(usuario)  # Sobrescribe el documento
        return {"success": True}
