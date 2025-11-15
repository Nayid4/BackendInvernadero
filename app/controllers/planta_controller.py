from flask import Blueprint, request, jsonify
from flask_problem_details import ProblemDetails, ProblemDetailsError
from flask_jwt_extended import jwt_required
from mediatr import Mediator

from application.plantas.commands.cambiar_estado_planta.dto import CambiarEstadoPlantaDTO
from application.plantas.commands.create_planta.dto import CreatePlantaDTO
from application.plantas.commands.update_planta.dto import UpdatePlantaDTO
from application.plantas.commands.delete_planta.dto import DeletePlantaDTO
from application.plantas.queries.consultar_planta_activa.dto import ConsultarPlantaActivaDTO
from application.plantas.queries.get_all_plantas.dto import GetAllPlantasDTO
from application.plantas.queries.get_planta_by_id.dto import GetPlantaByIdDTO
from application.plantas.queries.get_all_plantas.handler import GetAllPlantasHandler

planta_bp = Blueprint('planta', __name__)

@planta_bp.route('', methods=['POST'])
@jwt_required()
def create():
    dto = CreatePlantaDTO(**request.json)
    try:
        return jsonify(Mediator.send(dto)), 201
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error al crear planta",
                detail=str(e)
            )
        )

@planta_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    dto = GetPlantaByIdDTO(id)
    result = Mediator.send(dto)
    if not result:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Planta no encontrada",
                detail="No existe una planta con ese ID"
            )
        )
    return jsonify(result.to_dict()), 200

@planta_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update(id):
    dto = UpdatePlantaDTO(id=id, **request.json)
    try:
        return jsonify(Mediator.send(dto)), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error de actualización",
                detail=str(e)
            )
        )

@planta_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    dto = DeletePlantaDTO(id)
    try:
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

@planta_bp.route('', methods=['GET'])
#@jwt_required()
def get_all():
    try:
        dto = GetAllPlantasDTO()
        plantas = Mediator.send(dto)
        return jsonify(plantas), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error al obtener plantas",
                detail=str(e)
            )
        )

@planta_bp.route('/estado/<id>', methods=['PUT'])
@jwt_required()
def actualizar_estado(id):
    try:
        data = request.json
        dto = CambiarEstadoPlantaDTO(id=id, estado=data.get("estado"))
        result = Mediator.send(dto)
        return jsonify(result), 200
    except Exception as e:
        from flask_problem_details import ProblemDetails, ProblemDetailsError
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error al actualizar estado de la planta",
                detail=str(e)
            )
        )

@planta_bp.route('/activa', methods=['GET'])
@jwt_required()
def get_planta_activa():
    try:
        dto = ConsultarPlantaActivaDTO()
        result = Mediator.send(dto)
        if not result:
            raise ProblemDetailsError(
                ProblemDetails(
                    status=404,
                    title="No hay planta en estado activo",
                    detail="Actualmente no existe ninguna planta activa para monitoreo. Por favor active una planta desde la administración."
                )
            )
        return jsonify(result), 200
    except ProblemDetailsError as e:
        raise e  # DEJA que Flask y ProblemDetails lo manejen
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=500,
                title="Error consultando planta activa",
                detail=str(e),
            )
        )