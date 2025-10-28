from domain.usuario import Usuario
from infrastructure.firebase.firebase_client import db
from typing import List, Optional

class UsuarioRepository:
    COLLECTION_NAME = "usuarios"

    def guardar_usuario(self, usuario: Usuario):
        ref = db.collection(self.COLLECTION_NAME).document(usuario.id)
        ref.set({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "telefono": usuario.telefono,
            "rol": usuario.rol,
            "correo": usuario.correo,
            "contrasena_hash": usuario.contrasena_hash
        })

    def obtener_usuario_por_id(self, usuario_id: str) -> Optional[Usuario]:
        doc = db.collection(self.COLLECTION_NAME).document(usuario_id).get()
        if doc.exists:
            data = doc.to_dict()
            return Usuario(
                id=data['id'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                telefono=data['telefono'],
                correo=data['correo'],
                contrasena_hash=data['contrasena_hash'],
                rol=data.get('rol', 'user')
            )
        return None

    def obtener_usuario_por_correo(self, correo: str) -> Optional[Usuario]:
        docs = db.collection(self.COLLECTION_NAME).where("correo", "==", correo).stream()
        for doc in docs:
            data = doc.to_dict()
            return Usuario(
                id=data['id'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                telefono=data['telefono'],
                rol=data.get('rol', 'user'),
                correo=data['correo'],
                contrasena_hash=data['contrasena_hash']
            )
        return None


    def eliminar_usuario(self, correo: str):
        db.collection(self.COLLECTION_NAME).document(correo).delete()

    def obtener_todos_los_usuarios(self) -> List[dict]:
        docs = db.collection(self.COLLECTION_NAME).stream()
        usuarios = []
        for doc in docs:
            data = doc.to_dict()
            usuarios.append({
                "id": data.get('id'),
                "nombre": data.get('nombre'),
                "apellido": data.get('apellido'),
                "telefono": data.get('telefono'),
                "correo": data.get('correo'),
                "rol": data.get('rol')
            })
        return usuarios
