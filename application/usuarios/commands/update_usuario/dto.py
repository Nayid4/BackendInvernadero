class UpdateUsuarioDTO:
    def __init__(self, id, nombre=None, apellido=None, telefono=None, rol=None, correo=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.rol = rol
        self.correo = correo
