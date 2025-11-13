class Planta:
    def __init__(self, id, nombre, fecha_siembra):
        self.id = id
        self.nombre = nombre
        self.fecha_siembra = fecha_siembra  # esperado como string 'YYYY-MM-DD'

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_siembra": self.fecha_siembra
        }