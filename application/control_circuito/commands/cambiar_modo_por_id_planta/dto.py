class SetCircuitControlDTO:
    def __init__(self, idPlanta, modo, ventilador=None, rociador=None, luminosidad=None):
        self.idPlanta = idPlanta
        self.modo = modo
        self.ventilador = ventilador
        self.rociador = rociador
        self.luminosidad = luminosidad