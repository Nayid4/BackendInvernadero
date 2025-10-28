import os
import firebase_admin
from firebase_admin import credentials, firestore

# Singleton config (solo una vez)
if not firebase_admin._apps:
    firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")

    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
