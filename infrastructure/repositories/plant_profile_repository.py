import os
import glob
import csv
from statistics import mean

class PlantDatasetRepository:
    """
    Lee y procesa datos de múltiples CSV por planta, incluyendo todas las variables nuevas.
    """
    def get_plant_profile(self, planta: str):
        # 1. Dirección del directorio con los CSV
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../infrastructure
        data_dir = os.path.join(base_dir, "data")
        
        # 2. Búsqueda de archivos correspondientes a la planta
        plant_variants = [planta, planta.lower(), planta.capitalize()]
        files = set()
        for prefix in plant_variants:
            pattern = os.path.join(data_dir, f"{prefix}_*.csv")
            files.update(glob.glob(pattern))
        if not files:
            raise FileNotFoundError(f"No hay archivos CSV para la planta '{planta}' en {data_dir}")

        # 3. Leer todos los datos de todos los csv
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
                            'luminosidad': float(row['luminosidad']),
                            'ventilador': float(row['ventilador']),
                            'rociador': float(row['rociador']),
                            'temperatura_nivel': row['temperatura_nivel'],
                            'humedad_aire_nivel': row['humedad_aire_nivel'],
                            'humedad_suelo_nivel': row['humedad_suelo_nivel'],
                            'luminosidad_nivel': row['luminosidad_nivel'],
                            'ventilador_nivel': row['ventilador_nivel'],
                            'rociador_nivel': row['rociador_nivel'],
                            'recomendacion': row.get('recomendacion', '').strip()
                        })
                    except Exception as e:
                        print(f"Error en {file_path}: {e}")
                        continue

        if not all_data:
            raise ValueError(f"No se pudieron cargar datos válidos para la planta '{planta}'.")

        # 4. Cálculo de rangos y promedios (centroide) para nuevas variables
        def col_values(col): return [d[col] for d in all_data]
        temp_min, temp_max = min(col_values('temperatura')), max(col_values('temperatura'))
        hum_aire_min, hum_aire_max = min(col_values('humedad_aire')), max(col_values('humedad_aire'))
        hum_suelo_min, hum_suelo_max = min(col_values('humedad_suelo')), max(col_values('humedad_suelo'))
        luz_min, luz_max = min(col_values('luminosidad')), max(col_values('luminosidad'))
        vent_min, vent_max = min(col_values('ventilador')), max(col_values('ventilador'))
        roc_min, roc_max = min(col_values('rociador')), max(col_values('rociador'))

        centroide = {
            "temperatura": mean(col_values('temperatura')),
            "humedad_aire": mean(col_values('humedad_aire')),
            "humedad_suelo": mean(col_values('humedad_suelo')),
            "luminosidad": mean(col_values('luminosidad')),
            "ventilador": mean(col_values('ventilador')),
            "rociador": mean(col_values('rociador'))
        }
        # 5. Reglas completas (representa todas las combinaciones para lógica difusa)
        rules = []
        for d in all_data:
            rule = {
                "temperatura_nivel": d['temperatura_nivel'],
                "humedad_aire_nivel": d['humedad_aire_nivel'],
                "humedad_suelo_nivel": d['humedad_suelo_nivel'],
                "luminosidad_nivel": d['luminosidad_nivel'],
                "ventilador_nivel": d['ventilador_nivel'],
                "rociador_nivel": d['rociador_nivel'],
                "recomendacion": d['recomendacion']
            }
            rules.append(rule)

        return {
            "centroide": centroide,
            "temp_range": (temp_min, temp_max),
            "hum_aire_range": (hum_aire_min, hum_aire_max),
            "hum_suelo_range": (hum_suelo_min, hum_suelo_max),
            "luminosidad_range": (luz_min, luz_max),
            "ventilador_range": (vent_min, vent_max),
            "rociador_range": (roc_min, roc_max),
            "rules": rules,
            "archivos": list(files)
        }
