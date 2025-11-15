class UpdatePlantaDTO:
    def __init__(self, id, nombre=None, fecha_siembra=None, estado=None):
        self.id = id
        self.nombre = nombre
        self.fecha_siembra = fecha_siembra
        self.estado = estado
