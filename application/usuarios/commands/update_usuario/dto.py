class UpdateUsuarioDTO:
    def __init__(self, correo, nombre=None, apellido=None, telefono=None):
        self.correo = correo
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
