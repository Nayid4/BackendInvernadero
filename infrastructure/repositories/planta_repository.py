from domain.planta import Planta
from infrastructure.firebase.firebase_client import firestore_db as db
from typing import List, Optional
import uuid

class PlantaRepository:
    COLLECTION_NAME = "plantas"

    def guardar_planta(self, planta: Planta):
        # Si la planta no tiene id, asigna uno (para POST)
        planta_id = planta.id or str(uuid.uuid4())
        ref = db.collection(self.COLLECTION_NAME).document(planta_id)
        ref.set({
            "id": planta_id,
            "nombre": planta.nombre,
            "especie": planta.especie,
            "fecha_siembra": planta.fecha_siembra,
            "ubicacion": planta.ubicacion
        })

    def obtener_planta_por_id(self, planta_id: str) -> Optional[Planta]:
        doc = db.collection(self.COLLECTION_NAME).document(planta_id).get()
        if doc.exists:
            data = doc.to_dict()
            return Planta(
                id=data['id'],
                nombre=data['nombre'],
                especie=data['especie'],
                fecha_siembra=data['fecha_siembra'],
                ubicacion=data['ubicacion']
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
                "especie": data.get('especie'),
                "fecha_siembra": data.get('fecha_siembra'),
                "ubicacion": data.get('ubicacion')
            })
        return plantas
