from infrastructure.firebase.firebase_client import realtime_db
from domain.dtos.datos_ambiente_dto import DatosAmbienteDTO
from typing import List, Optional

class DatosAmbienteRepository:
    def get_historico_completo(self) -> List[DatosAmbienteDTO]:
        raw = realtime_db.child('invernadero').get()
        if not raw or "historico" not in raw or not isinstance(raw["historico"], dict):
            return []
        historico = raw["historico"]
        resultado = []
        for ts, datos in historico.items():
            try:
                resultado.append(
                    DatosAmbienteDTO(
                        timestamp=ts,
                        temperatura=float(datos['temperatura']),
                        humedad_ambiental=float(datos['humedad_ambiental']),
                        humedad_suelo=float(datos['humedad_suelo'])
                    )
                )
            except (KeyError, ValueError, TypeError):
                continue
        return resultado

    def get_ultimo_registro(self) -> Optional[DatosAmbienteDTO]:
        historicos = self.get_historico_completo()
        if not historicos:
            return None
        return max(historicos, key=lambda d: d.timestamp)
