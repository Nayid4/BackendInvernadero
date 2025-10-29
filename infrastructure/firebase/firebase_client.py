import os
import firebase_admin
from firebase_admin import credentials, firestore, db

# Cargar ruta de credencial y URL de realtime desde .env
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")
firebase_realtime_url = os.getenv("FIREBASE_REALTIME_URL")

# Singleton config (solo una vez)
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': firebase_realtime_url
    })

firestore_db = firestore.client()
realtime_db = db.reference()  # Punto de entrada al realtime database, puedes parametrizar el path
