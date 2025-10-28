class CreateUsuarioDTO:
    def __init__(self, nombre, apellido, telefono, correo, contrasena):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena
