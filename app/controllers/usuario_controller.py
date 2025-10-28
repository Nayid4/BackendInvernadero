from flask import Blueprint, request, jsonify
from mediatr import Mediator
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_problem_details import ProblemDetails, ProblemDetailsError

from application.usuarios.commands.create_usuario.dto import CreateUsuarioDTO
from application.usuarios.commands.delete_usuario.dto import DeleteUsuarioDTO
from application.usuarios.commands.update_usuario.dto import UpdateUsuarioDTO
from application.usuarios.queries.get_all_usuarios.dto import GetAllUsuariosDTO
from application.usuarios.queries.get_all_usuarios.handler import GetAllUsuariosHandler
from application.usuarios.queries.get_usuario_by_id.dto import GetUsuarioByIdDTO
from application.usuarios.queries.get_usuario_by_correo.dto import GetUsuarioByCorreoDTO
from application.usuarios.queries.login.dto import LoginUsuarioDTO

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    dto = LoginUsuarioDTO(correo=data['correo'], contrasena=data['contrasena'])
    try:
        return jsonify(Mediator.send(dto)), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=401,
                title="Error de autenticación",
                detail=str(e)
            )
        )

@usuario_bp.route('/refresh', methods=['POST'])
#@jwt_required(refresh=True)
def refresh():
    usuario_id = get_jwt_identity()
    access_token = create_access_token(identity=usuario_id)
    return jsonify(access_token=access_token), 200

@usuario_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    usuario_id = get_jwt_identity()
    dto = GetUsuarioByIdDTO(usuario_id)
    usuario = Mediator.send(dto)
    if not usuario:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Usuario no encontrado",
                detail="No se encontró el usuario asociado al token"
            )
        )
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "telefono": usuario.telefono,
        "correo": usuario.correo,
        "rol": usuario.rol
    }), 200

@usuario_bp.route('', methods=['POST'])
def register():
    try:
        dto = CreateUsuarioDTO(**request.json)
        return jsonify(Mediator.send(dto)), 201
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error de registro",
                detail=str(e)
            )
        )

@usuario_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update(id):
    try:
        dto = UpdateUsuarioDTO(id=id, **request.json)
        return jsonify(Mediator.send(dto)), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error de actualización",
                detail=str(e)
            )
        )

@usuario_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        dto = DeleteUsuarioDTO(id)
        Mediator.send(dto)
        return '', 204
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error de eliminación",
                detail=str(e)
            )
        )

@usuario_bp.route('/by-email/<correo>', methods=['GET'])
@jwt_required()
def get_by_email(correo):
    dto = GetUsuarioByCorreoDTO(correo)
    usuario = Mediator.send(dto)
    if not usuario:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Usuario no encontrado",
                detail="No existe un usuario con ese correo"
            )
        )
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "telefono": usuario.telefono,
        "correo": usuario.correo,
        "rol": usuario.rol
    }), 200

@usuario_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    dto = GetUsuarioByIdDTO(id)
    usuario = Mediator.send(dto)
    if not usuario:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Usuario no encontrado",
                detail="No existe un usuario con ese id"
            )
        )
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "telefono": usuario.telefono,
        "correo": usuario.correo,
        "rol": usuario.rol
    }), 200


@usuario_bp.route('', methods=['GET'])
#@jwt_required()
def get_all():
    try:
        dto = GetAllUsuariosDTO()
        usuarios = Mediator.send(dto)
        return jsonify(usuarios), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error al obtener usuarios",
                detail=str(e)
            )
        )
