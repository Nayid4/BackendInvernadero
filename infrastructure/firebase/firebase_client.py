import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, db

# Cargar ruta de credencial y URL de realtime desde .env
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")
firebase_json_content = os.getenv('FIREBASE_CREDENTIALS_JSON')
firebase_realtime_url = os.getenv("FIREBASE_REALTIME_URL")

# Singleton config (solo una vez)
if not firebase_admin._apps:
    firebase_credentials = json.loads(firebase_json_content)
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred, {
        'databaseURL': firebase_realtime_url
    })

firestore_db = firestore.client()
realtime_db = db.reference()  # Punto de entrada al realtime database, puedes parametrizar el path
