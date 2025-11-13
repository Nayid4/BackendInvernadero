class ControlByIdRequestDTO:
    def __init__(self, idPlanta, temperatura, humedad_aire, humedad_suelo):
        self.idPlanta = idPlanta
        self.temperatura = float(temperatura)
        self.humedad_aire = float(humedad_aire)
        self.humedad_suelo = float(humedad_suelo)
