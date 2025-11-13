import os
import uuid
import csv

PLANTAS_ESPECIES = ["Tomate", "Lechuga", "Pimenton"]
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
EXPECTED_HEADERS = ["planta", "temperatura", "humedad_aire", "humedad_suelo", "ventilador", "rociador", "luminosidad"]

class CsvDatasetRepository:
    def validar_csv(self, stream):
        # Lee la primera línea del archivo CSV para validar estructura (sin leer todo)
        stream.seek(0)
        reader = csv.reader(stream.read().decode("utf-8").splitlines())
        headers = next(reader)
        return headers == EXPECTED_HEADERS

    def archivo_con_especie_valida(self, nombre):
        nombre_lower = nombre.lower()
        return any(e.lower() in nombre_lower for e in PLANTAS_ESPECIES)

    def agregar_archivo(self, file_storage):
        if not file_storage or not file_storage.filename.endswith('.csv'):
            raise Exception("Solo se permiten archivos CSV.")
        if not self.archivo_con_especie_valida(file_storage.filename):
            raise Exception(f"El nombre del archivo debe contener alguna especie válida: {PLANTAS_ESPECIES}")
        # Validar estructura CSV
        if not self.validar_csv(file_storage.stream):
            raise Exception("El archivo CSV no tiene el formato esperado.")
        file_id = str(uuid.uuid4())
        filename = f"{os.path.splitext(file_storage.filename)[0]}_{file_id}.csv"
        path = os.path.join(DATA_DIR, filename)
        file_storage.save(path)
        return filename

    def listar_archivos(self):
        archivos = []
        for f in os.listdir(DATA_DIR):
            if f.endswith('.csv') and self.archivo_con_especie_valida(f):
                archivos.append(f)
        return archivos

    def descargar_archivo(self, filename):
        path = os.path.join(DATA_DIR, filename)
        if not os.path.isfile(path):
            raise Exception("Archivo no encontrado.")
        return path

    def eliminar_archivo(self, filename):
        path = os.path.join(DATA_DIR, filename)
        if not os.path.isfile(path):
            raise Exception("Archivo no encontrado.")
        os.remove(path)
        return True