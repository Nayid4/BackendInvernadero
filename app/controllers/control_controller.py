from flask import Blueprint, request, jsonify
from mediatr import Mediator
from flask_jwt_extended import jwt_required
from flask_problem_details import ProblemDetails, ProblemDetailsError

from application.controles.queries.consultar_control.dto import ControlRequestDTO
from application.controles.queries.get_historico.dto import GetHistoricoDTO

control_bp = Blueprint('control', __name__)

@control_bp.route('/consultar', methods=['POST'])
def control():
    try:
        data = request.json
        dto = ControlRequestDTO(
            temperatura=data['temperatura'],
            humedad_aire=data['humedad_aire'],
            humedad_suelo=data['humedad_suelo'],
            planta=data['planta']
        )
        result = Mediator.send(dto)
        if result is None:
            raise ProblemDetailsError(ProblemDetails(
                status=404,
                title="Acción no determinada",
                detail="No se pudo calcular la acción para los actuadores"
            ))
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(ProblemDetails(
            status=500,
            title="Error de la lógica difusa",
            detail=str(e)
        ))

@control_bp.route('/historico', methods=['GET'])
#@jwt_required()
def consultar_historico():
    dto = GetHistoricoDTO()
    try:
        result = Mediator.send(dto)
        if not result or len(result) == 0:
            raise ProblemDetailsError(
                ProblemDetails(
                    status=404,
                    title="Histórico no encontrado",
                    detail="No se encontraron registros históricos de ambiente en la base de datos"
                )
            )
        return jsonify(result), 200
    except ProblemDetailsError as e:
        # Deja que ProblemDetails maneje el error, no lo encierres en un 500
        raise e
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=500,
                title="Error al consultar histórico",
                detail=str(e)
            )
        )
