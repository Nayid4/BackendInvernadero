import os
import glob
import csv
import math

class PlantDatasetRepository:
    """
    Lee y procesa datos de múltiples archivos CSV por planta.
    Además, calcula:
    - universe_of_discourse: min-max completo de cada variable
    - valores óptimos: rango del percentil 25-75 para cada variable
    """

    def get_plant_profile(self, planta: str):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../infrastructure
        data_dir = os.path.join(base_dir, "data")

        # Archivos que pueden contener datos de la planta
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

        def col_values(col):
            return [d[col] for d in all_data]

        # Función para calcular percentil sin librerías externas
        def percentil_manual(lst, pct):
            lst_sorted = sorted(lst)
            k = int(math.ceil(pct * len(lst))) - 1
            return lst_sorted[max(0, min(k, len(lst)-1))]

        # Calcular rango óptimo basado en percentiles 25 y 75
        def calcular_rango_optimo(lst):
            p25 = percentil_manual(lst, 0.25)
            p75 = percentil_manual(lst, 0.75)
            return (round(p25, 2), round(p75, 2))

        # Obtener listas de valores para las variables
        temp_values = col_values('temperatura')
        hum_aire_values = col_values('humedad_aire')
        hum_suelo_values = col_values('humedad_suelo')
        luz_values = col_values('luminosidad')

        perfil = {
            "centroide": {
                "temperatura": sum(temp_values) / len(temp_values),
                "humedad_aire": sum(hum_aire_values) / len(hum_aire_values),
                "humedad_suelo": sum(hum_suelo_values) / len(hum_suelo_values),
                "luminosidad": sum(luz_values) / len(luz_values),
                "ventilador": sum(col_values('ventilador')) / len(all_data),
                "rociador": sum(col_values('rociador')) / len(all_data),
            },
            # Total range para cada variable: universe_of_discourse
            "universe_of_discourse": {
                "temp_range": (min(temp_values), max(temp_values)),
                "hum_aire_range": (min(hum_aire_values), max(hum_aire_values)),
                "hum_suelo_range": (min(hum_suelo_values), max(hum_suelo_values)),
                "luminosidad_range": (min(luz_values), max(luz_values))
            },
            # Rango óptimo calculado con percentiles 25-75
            "optimos_range": {
                "temp_range": calcular_rango_optimo(temp_values),
                "hum_aire_range": calcular_rango_optimo(hum_aire_values),
                "hum_suelo_range": calcular_rango_optimo(hum_suelo_values),
                "luminosidad_range": calcular_rango_optimo(luz_values)
            },
            "archivos": list(files),
            "datos": all_data  # Puedes remover si solo quieres datos agregados
        }

        return perfil
