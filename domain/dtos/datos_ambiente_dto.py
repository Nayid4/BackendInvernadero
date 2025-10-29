from dataclasses import dataclass

@dataclass
class DatosAmbienteDTO:
    timestamp: str
    temperatura: float
    humedad_ambiental: float
    humedad_suelo: float
