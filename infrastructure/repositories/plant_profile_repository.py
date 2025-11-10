import os
import glob
import csv
from statistics import mean

class PlantDatasetRepository:
    def get_plant_profile(self, planta: str):
        # Busca la carpeta 'data' estando en infrastructure/repositories
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Sube a /infrastructure
        data_dir = os.path.join(base_dir, "data") # Ahora es /infrastructure/data

        plant_prefixes = [planta, planta.lower(), planta.capitalize()]
        files = set()
        for prefix in plant_prefixes:
            pattern = os.path.join(data_dir, f"{prefix}_*.csv")
            files.update(glob.glob(pattern))

        if not files:
            raise FileNotFoundError(f"No hay archivos CSV para la planta '{planta}' en {data_dir}")

        all_data = []
        for file_path in files:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        all_data.append({
                            'temperatura': float(row['temperatura']),
                            'humedad_aire': float(row['humedad_aire']),
                            'humedad_suelo': float(row['humedad_suelo']),
                            'temperatura_nivel': row['temperatura_nivel'],
                            'humedad_aire_nivel': row['humedad_aire_nivel'],
                            'humedad_suelo_nivel': row['humedad_suelo_nivel'],
                            'recomendacion': row.get('recomendacion', '').strip()
                        })
                    except Exception as e:
                        print(f"Error en {file_path}: {e}")
                        continue

        if not all_data:
            raise ValueError(f"No se pudieron cargar datos válidos para la planta '{planta}'.")

        temps = [d['temperatura'] for d in all_data]
        hum_aires = [d['humedad_aire'] for d in all_data]
        hum_suelos = [d['humedad_suelo'] for d in all_data]

        temp_min, temp_max = min(temps), max(temps)
        hum_aire_min, hum_aire_max = min(hum_aires), max(hum_aires)
        hum_suelo_min, hum_suelo_max = min(hum_suelos), max(hum_suelos)

        centroide = {
            "temperatura": mean(temps),
            "humedad_aire": mean(hum_aires),
            "humedad_suelo": mean(hum_suelos)
        }

        rules = [{
            "temperatura_nivel": d['temperatura_nivel'],
            "humedad_aire_nivel": d['humedad_aire_nivel'],
            "humedad_suelo_nivel": d['humedad_suelo_nivel'],
            "recomendacion": d['recomendacion']
        } for d in all_data]

        return {
            "centroide": centroide,
            "temp_range": (temp_min, temp_max),
            "hum_aire_range": (hum_aire_min, hum_aire_max),
            "hum_suelo_range": (hum_suelo_min, hum_suelo_max),
            "rules": rules,
            "archivos": list(files)
        }
