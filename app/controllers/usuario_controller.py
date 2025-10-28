from flask import Blueprint, request, jsonify
from mediatr import Mediator
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_problem_details import problem_details

from application.usuarios.commands.create_usuario.dto import CreateUsuarioDTO
from application.usuarios.commands.delete_usuario.dto import DeleteUsuarioDTO
from application.usuarios.commands.update_usuario.dto import UpdateUsuarioDTO
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
        return problem_details(
            title="Error de autenticación",
            status=401,
            detail=str(e)
        ), 401

@usuario_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    usuario_id = get_jwt_identity()
    dto = GetUsuarioByIdDTO(usuario_id)
    usuario = Mediator.send(dto)
    if not usuario:
        return problem_details(
            title="Usuario no encontrado",
            status=404,
            detail="No se encontró el usuario asociado al token"
        ), 404
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "telefono": usuario.telefono,
        "correo": usuario.correo,
        "rol": usuario.rol
    }), 200

@usuario_bp.route('/', methods=['POST'])
def register():
    try:
        dto = CreateUsuarioDTO(**request.json)
        return jsonify(Mediator.send(dto)), 201
    except Exception as e:
        return problem_details(
            title="Error de registro",
            status=400,
            detail=str(e)
        ), 400

@usuario_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update(id):
    try:
        dto = UpdateUsuarioDTO(id=id, **request.json)
        return jsonify(Mediator.send(dto)), 200
    except Exception as e:
        return problem_details(
            title="Error de actualización",
            status=400,
            detail=str(e)
        ), 400

@usuario_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    try:
        dto = DeleteUsuarioDTO(id)
        Mediator.send(dto)
        return '', 204
    except Exception as e:
        return problem_details(
            title="Error de eliminación",
            status=400,
            detail=str(e)
        ), 400

@usuario_bp.route('/by-email/<correo>', methods=['GET'])
@jwt_required()
def get_by_email(correo):
    dto = GetUsuarioByCorreoDTO(correo)
    usuario = Mediator.send(dto)
    if not usuario:
        return problem_details(
            title="Usuario no encontrado",
            status=404,
            detail="No existe un usuario con ese correo"
        ), 404
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "telefono": usuario.telefono,
        "correo": usuario.correo,
        "rol": usuario.rol
    }), 200

@usuario_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    try:
        usuarios = Mediator.send(GetAllUsuariosHandler())
        return jsonify(usuarios), 200
    except Exception as e:
        return problem_details(
            title="Error al obtener usuarios",
            status=400,
            detail=str(e)
        ), 400
