# infrastructure/repositories/circuit_control_repository.py
from infrastructure.firebase.firebase_client import firestore_db as db

class CircuitControlRepository:
    COLLECTION_NAME = "circuit_control_mode"

    def set_control_mode(self, idPlanta, modo, ventilador=None, rociador=None, luminosidad=None):
        data = {"modo": modo}
        if modo == "manual":
            data.update({"ventilador": ventilador, "rociador": rociador, "luminosidad": luminosidad})
        ref = db.collection(self.COLLECTION_NAME).document(idPlanta)
        ref.set(data)

    def get_control_mode(self, idPlanta):
        doc = db.collection(self.COLLECTION_NAME).document(idPlanta).get()
        return doc.to_dict() if doc.exists else None
    
    def eliminar_control_mode(self, idPlanta):
        db.collection(self.COLLECTION_NAME).document(idPlanta).delete()
