class UpdatePlantaDTO:
    def __init__(self, id, nombre=None, especie=None, fecha_siembra=None, ubicacion=None):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.fecha_siembra = fecha_siembra
        self.ubicacion = ubicacion
