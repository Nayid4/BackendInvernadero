class CreateUsuarioDTO:
    def __init__(self, nombre, apellido, telefono, rol, correo, contrasena):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.rol = rol
        self.correo = correo
        self.contrasena = contrasena
