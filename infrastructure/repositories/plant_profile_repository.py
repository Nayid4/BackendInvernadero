import os
import glob
import csv
from statistics import mean

class PlantDatasetRepository:
    """
    Lee y procesa datos de múltiples archivos CSV por planta.
    """
    def get_plant_profile(self, planta: str):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../infrastructure
        data_dir = os.path.join(base_dir, "data")

        # Incluye archivos "pimenton.csv", "pimenton_*.csv" y similares
        plant_variants = [planta.lower(), planta.capitalize(), planta]
        files = set()
        for prefix in plant_variants:
            pattern_csv = os.path.join(data_dir, f"{prefix}.csv")
            pattern_any = os.path.join(data_dir, f"{prefix}_*.csv")
            files.update(glob.glob(pattern_csv))
            files.update(glob.glob(pattern_any))

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
                            'luminosidad': float(row.get('luminosidad', 0)),
                            'ventilador': float(row.get('ventilador', 0)),
                            'rociador': float(row.get('rociador', 0)),
                            'planta': row.get('planta', planta)
                        })
                    except Exception as e:
                        print(f"Error en {file_path}: {e}")
                        continue

        if not all_data:
            raise ValueError(f"No se pudieron cargar datos válidos para la planta '{planta}'.")

        def col_values(col): return [d[col] for d in all_data]

        perfil = {
            "centroide": {
                "temperatura": mean(col_values('temperatura')),
                "humedad_aire": mean(col_values('humedad_aire')),
                "humedad_suelo": mean(col_values('humedad_suelo')),
                "luminosidad": mean(col_values('luminosidad')),
                "ventilador": mean(col_values('ventilador')),
                "rociador": mean(col_values('rociador')),
            },
            "temp_range": (min(col_values('temperatura')), max(col_values('temperatura'))),
            "hum_aire_range": (min(col_values('humedad_aire')), max(col_values('humedad_aire'))),
            "hum_suelo_range": (min(col_values('humedad_suelo')), max(col_values('humedad_suelo'))),
            "luminosidad_range": (min(col_values('luminosidad')), max(col_values('luminosidad'))),
            "ventilador_range": (min(col_values('ventilador')), max(col_values('ventilador'))),
            "rociador_range": (min(col_values('rociador')), max(col_values('rociador'))),
            "archivos": list(files),
            "datos": all_data  # puedes remover esto si solo quieres medidas agregadas
        }
        return perfil
