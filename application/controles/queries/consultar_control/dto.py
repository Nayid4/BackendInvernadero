class ControlRequestDTO:
    def __init__(self, temperatura, humedad_aire, humedad_suelo, planta):
        self.temperatura = float(temperatura)
        self.humedad_aire = float(humedad_aire)
        self.humedad_suelo = float(humedad_suelo)
        self.planta = planta
