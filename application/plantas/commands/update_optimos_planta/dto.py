class UpdateOptimosPlantaDTO:
    def __init__(self, idPlanta, temp_range, hum_suelo_range, hum_aire_range, luz_range):
        self.idPlanta = idPlanta
        self.temp_range = temp_range
        self.hum_suelo_range = hum_suelo_range
        self.hum_aire_range = hum_aire_range
        self.luz_range = luz_range