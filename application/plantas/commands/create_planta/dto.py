class CreatePlantaDTO:
    def __init__(self, nombre, fecha_siembra, estado="Desactivo"):
        self.nombre = nombre
        self.fecha_siembra = fecha_siembra
        self.estado = estado