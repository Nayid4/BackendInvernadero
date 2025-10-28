class CreatePlantaDTO:
    def __init__(self, nombre, especie, fecha_siembra, ubicacion, usuario_id):
        self.nombre = nombre
        self.especie = especie
        self.fecha_siembra = fecha_siembra
        self.ubicacion = ubicacion
        self.usuario_id = usuario_id
