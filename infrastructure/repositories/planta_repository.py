from domain.planta import Planta
from infrastructure.firebase.firebase_client import firestore_db as db
from typing import List, Optional
import uuid

class PlantaRepository:
    COLLECTION_NAME = "plantas"

    def guardar_planta(self, planta: Planta):
        planta_id = planta.id or str(uuid.uuid4())
        ref = db.collection(self.COLLECTION_NAME).document(planta_id)
        ref.set({
            "id": planta_id,
            "nombre": planta.nombre,
            "fecha_siembra": planta.fecha_siembra,
        })
        if planta.id is None:
            planta.id = planta_id  # Asigna el id generado de vuelta al objeto


    def actualizar_planta(self, planta: Planta):
        if not planta.id:
            raise Exception("No se puede actualizar: falta id.")
        ref = db.collection(self.COLLECTION_NAME).document(planta.id)
        ref.update({
            "nombre": planta.nombre,
            "fecha_siembra": planta.fecha_siembra,
        })

    def obtener_planta_por_id(self, planta_id: str) -> Optional[Planta]:
        doc = db.collection(self.COLLECTION_NAME).document(planta_id).get()
        if doc.exists:
            data = doc.to_dict()
            return Planta(
                id=data['id'],
                nombre=data['nombre'],
                fecha_siembra=data['fecha_siembra'],
            )
        return None

    def eliminar_planta(self, planta_id: str):
        db.collection(self.COLLECTION_NAME).document(planta_id).delete()

    def obtener_todas_las_plantas(self) -> List[dict]:
        docs = db.collection(self.COLLECTION_NAME).stream()
        plantas = []
        for doc in docs:
            data = doc.to_dict()
            plantas.append({
                "id": data.get('id'),
                "nombre": data.get('nombre'),
                "fecha_siembra": data.get('fecha_siembra'),
            })
        return plantas
