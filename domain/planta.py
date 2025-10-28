class Planta:
    def __init__(self, id, nombre, especie, fecha_siembra, ubicacion, usuario_id=None):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.fecha_siembra = fecha_siembra  # esperado como string 'YYYY-MM-DD'
        self.ubicacion = ubicacion
        self.usuario_id = usuario_id
