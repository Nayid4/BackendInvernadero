from flask import Blueprint, jsonify
from mediatr import Mediator
from flask_jwt_extended import jwt_required
from flask_problem_details import ProblemDetails, ProblemDetailsError

from application.abanico.queries.consultar_abanico.dto import ConsultarAbanicoDTO
from application.abanico.queries.get_historico.dto import GetHistoricoDTO

abanico_bp = Blueprint('abanico', __name__)

@abanico_bp.route('/consultar', methods=['GET'])
@jwt_required()
def consultar():
    try:
        dto = ConsultarAbanicoDTO()
        result = Mediator.send(dto)
        if result is None:
            raise ProblemDetailsError(
                ProblemDetails(
                    status=404,
                    title="Datos no encontrados",
                    detail="No se encontraron datos ambientales recientes en la base de datos"
                )
            )
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=500,
                title="Error al consultar abanico",
                detail=str(e)
            )
        )

@abanico_bp.route('/historico', methods=['GET'])
@jwt_required()
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
