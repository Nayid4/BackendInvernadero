from infrastructure.firebase.firebase_client import realtime_db
from domain.dtos.datos_ambiente_dto import DatosAmbienteDTO
from typing import List, Optional

class DatosAmbienteRepository:
    def get_historico_completo(self) -> List[DatosAmbienteDTO]:
        historico = realtime_db.child('historico').get()
        if not historico or not isinstance(historico, dict):
            return []
        resultado = []
        for registro_id, datos in historico.items():
            try:
                resultado.append(
                    DatosAmbienteDTO(
                        id=registro_id,
                        fecha=datos.get('fecha', ''),
                        planta=datos.get('planta', ''),
                        temperatura=float(datos.get('temperatura', 0)),
                        humedad_aire=float(datos.get('humedad_aire', 0)),
                        humedad_suelo=float(datos.get('humedad_suelo', 0))
                    )
                )
            except (KeyError, ValueError, TypeError):
                continue
        return resultado

    def get_ultimo_registro(self) -> Optional[DatosAmbienteDTO]:
        historicos = self.get_historico_completo()
        if not historicos:
            return None
        # Ordena por fecha si es necesario, aquí se usa el orden lexicográfico del id
        return sorted(historicos, key=lambda d: d.id)[-1]
