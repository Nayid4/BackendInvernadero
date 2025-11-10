from dataclasses import dataclass
from typing import Optional

@dataclass
class DatosAmbienteDTO:
    id: str
    fecha: str
    planta: str
    temperatura: float
    humedad_aire: float
    humedad_suelo: float
