from flask import Blueprint, request, jsonify
from flask_problem_details import ProblemDetails, ProblemDetailsError
from flask_jwt_extended import jwt_required
from mediatr import Mediator

from application.control_circuito.commands.cambiar_modo_por_id_planta.dto import SetCircuitControlDTO
from application.control_circuito.quieries.consultar_modo_por_id_planta.dto import GetCircuitControlDTO

circuit_bp = Blueprint('circuit_control', __name__)

@circuit_bp.route('/control', methods=['PUT'])
@jwt_required()
def set_circuit_control():
    try:
        data = request.json
        dto = SetCircuitControlDTO(
            idPlanta=data["idPlanta"],
            modo=data["modo"],
            ventilador=data.get("ventilador"),
            rociador=data.get("rociador"),
            luminosidad=data.get("luminosidad")
        )
        result = Mediator.send(dto)
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error al configurar modo de circuito",
                detail=str(e)
            )
        )

@circuit_bp.route('control/<idPlanta>', methods=['GET'])
def get_circuit_control(idPlanta):
    try:
        dto = GetCircuitControlDTO(idPlanta)
        result = Mediator.send(dto)
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Error al consultar bandera de circuito",
                detail=str(e)
            )
        )
