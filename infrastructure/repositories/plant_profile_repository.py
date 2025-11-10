import os
import glob
import pandas as pd

class PlantDatasetRepository:
    def get_plant_profile(self, planta: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "../data")
        # Patrones que incluyen mayúsculas (Tomate_1.csv, tomate_1.csv, etc) para robustez
        pattern1 = os.path.join(data_dir, f"{planta}_*.csv")
        pattern2 = os.path.join(data_dir, f"{planta.lower()}_*.csv")
        pattern3 = os.path.join(data_dir, f"{planta.capitalize()}_*.csv")
        files = set(glob.glob(pattern1) + glob.glob(pattern2) + glob.glob(pattern3))
        if not files:
            raise FileNotFoundError(f"No hay archivos CSV para la planta '{planta}' en {data_dir}")
        dfs = [pd.read_csv(f) for f in files]
        df = pd.concat(dfs, ignore_index=True)
        temp_min, temp_max = df['temperatura'].min(), df['temperatura'].max()
        hum_aire_min, hum_aire_max = df['humedad_aire'].min(), df['humedad_aire'].max()
        hum_suelo_min, hum_suelo_max = df['humedad_suelo'].min(), df['humedad_suelo'].max()
        centroide = {
            "temperatura": df['temperatura'].mean(),
            "humedad_aire": df['humedad_aire'].mean(),
            "humedad_suelo": df['humedad_suelo'].mean()
        }
        rules = []
        for _, row in df.iterrows():
            rule = {
                "temperatura_nivel": row['temperatura_nivel'],
                "humedad_aire_nivel": row['humedad_aire_nivel'],
                "humedad_suelo_nivel": row['humedad_suelo_nivel'],
                "recomendacion": str(row.get('recomendacion', '')).strip()
            }
            rules.append(rule)
        return {
            "centroide": centroide,
            "temp_range": (temp_min, temp_max),
            "hum_aire_range": (hum_aire_min, hum_aire_max),
            "hum_suelo_range": (hum_suelo_min, hum_suelo_max),
            "rules": rules,
            "archivos": list(files)  # útil para depuración
        }
