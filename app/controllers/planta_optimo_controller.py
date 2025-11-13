# app/controllers/planta_optimos_bp.py
from flask import Blueprint, request, jsonify
from flask_problem_details import ProblemDetails, ProblemDetailsError
from flask_jwt_extended import jwt_required
from mediatr import Mediator

from application.plantas.commands.create_optimos_planta.dto import CreateOptimosPlantaDTO
from application.plantas.commands.update_optimos_planta.dto import UpdateOptimosPlantaDTO
from application.plantas.queries.consultar_optimos_planta.dto import GetOptimosPlantaDTO

planta_optimos_bp = Blueprint('planta_optimos', __name__)

@planta_optimos_bp.route('/', methods=['PUT'])
@jwt_required()
def update_optimos():
    try:
        datos = request.json
        dto = UpdateOptimosPlantaDTO(
            idPlanta=datos["idPlanta"],
            temp_range=datos["temp_range"],
            hum_suelo_range=datos["hum_suelo_range"],
            hum_aire_range=datos["hum_aire_range"],
            luz_range=datos["luz_range"]
        )
        result = Mediator.send(dto)
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error al actualizar valores óptimos",
                detail=str(e)
            )
        )

@planta_optimos_bp.route('/', methods=['POST'])
@jwt_required()
def create_optimos():
    try:
        datos = request.json
        dto = CreateOptimosPlantaDTO(
            idPlanta=datos["idPlanta"],
            temp_range=datos["temp_range"],
            hum_suelo_range=datos["hum_suelo_range"],
            hum_aire_range=datos["hum_aire_range"],
            luz_range=datos["luz_range"]
        )
        result = Mediator.send(dto)
        return jsonify(result), 201
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=409,
                title="Óptimos ya registrados",
                detail=str(e)
            )
        )

@planta_optimos_bp.route('/<idPlanta>', methods=['GET'])
@jwt_required()
def get_optimos_by_id(idPlanta):
    try:
        dto = GetOptimosPlantaDTO(idPlanta)
        datos = Mediator.send(dto)
        return jsonify(datos), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Valores óptimos no encontrados",
                detail=str(e)
            )
        )
