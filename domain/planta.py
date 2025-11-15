class Planta:
    def __init__(self, id, nombre, fecha_siembra, estado="Desactivo"):
        self.id = id
        self.nombre = nombre
        self.fecha_siembra = fecha_siembra  # string 'YYYY-MM-DD'
        self.estado = estado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_siembra": self.fecha_siembra,
            "estado": self.estado
        }
