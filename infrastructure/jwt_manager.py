from flask_jwt_extended import create_access_token

def generar_token(usuario_id):
    return create_access_token(identity=usuario_id)
