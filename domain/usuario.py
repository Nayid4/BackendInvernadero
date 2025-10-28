class Usuario:
    def __init__(self, id, nombre, apellido, telefono, rol, correo, contrasena_hash):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.rol = rol
        self.correo = correo
        self.contrasena_hash = contrasena_hash
