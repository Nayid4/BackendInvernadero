from domain.optimos_planta import OptimosPlanta
from infrastructure.firebase.firebase_client import firestore_db as db

class OptimosPlantaRepository:
    COLLECTION_NAME = "optimos_plantas"
    
    def guardar_optimos(self, optimos: OptimosPlanta):
        ref = db.collection(self.COLLECTION_NAME).document(optimos.idPlanta)
        ref.set({
            "idPlanta": optimos.idPlanta,
            "temp_range": optimos.temp_range,
            "hum_suelo_range": optimos.hum_suelo_range,
            "hum_aire_range": optimos.hum_aire_range,
            "luz_range": optimos.luz_range,
        })
    
    def obtener_optimos_por_id(self, idPlanta: str):
        doc = db.collection(self.COLLECTION_NAME).document(idPlanta).get()
        return doc.to_dict() if doc.exists else None

    def actualizar_optimos(self, optimos: OptimosPlanta):
        self.guardar_optimos(optimos)

    def ya_existen_optimos(self, idPlanta):
        doc = db.collection(self.COLLECTION_NAME).document(idPlanta).get()
        return doc.exists
    
    def eliminar_optimos(self, idPlanta):
        db.collection(self.COLLECTION_NAME).document(idPlanta).delete()