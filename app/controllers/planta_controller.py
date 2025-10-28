from flask import Blueprint, request, jsonify
from flask_problem_details import problem_details
from flask_jwt_extended import jwt_required
from mediatr import Mediator

from application.plantas.commands.create_planta.dto import CreatePlantaDTO
from application.plantas.commands.update_planta.dto import UpdatePlantaDTO
from application.plantas.commands.delete_planta.dto import DeletePlantaDTO
from application.plantas.queries.get_planta_by_id.dto import GetPlantaByIdDTO
from application.plantas.queries.get_all_plantas.handler import GetAllPlantasHandler

planta_bp = Blueprint('planta', __name__)

@planta_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    dto = CreatePlantaDTO(**request.json)
    try:
        return jsonify(Mediator.send(dto)), 201
    except Exception as e:
        return problem_details(
            title="Error al crear planta",
            status=400,
            detail=str(e)
        ), 400

@planta_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    dto = GetPlantaByIdDTO(id)
    result = Mediator.send(dto)
    if not result:
        return problem_details(
            title="Planta no encontrada",
            status=404,
            detail="No existe una planta con ese ID"
        ), 404
    return jsonify(result), 200

@planta_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update(id):
    dto = UpdatePlantaDTO(id=id, **request.json)
    try:
        return jsonify(Mediator.send(dto)), 200
    except Exception as e:
        return problem_details(
            title="Error de actualización",
            status=400,
            detail=str(e)
        ), 400

@planta_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    dto = DeletePlantaDTO(id)
    try:
        Mediator.send(dto)
        return '', 204
    except Exception as e:
        return problem_details(
            title="Error de eliminación",
            status=400,
            detail=str(e)
        ), 400

@planta_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    try:
        plantas = Mediator.send(GetAllPlantasHandler())
        return jsonify(plantas), 200
    except Exception as e:
        return problem_details(
            title="Error al obtener plantas",
            status=400,
            detail=str(e)
        ), 400
