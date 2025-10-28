class Usuario:
    def __init__(self, nombre, apellido, telefono, correo, contrasena_hash):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.contrasena_hash = contrasena_hash
