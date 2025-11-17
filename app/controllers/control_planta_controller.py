from flask import Blueprint, request, jsonify
from mediatr import Mediator
from flask_jwt_extended import jwt_required
from flask_problem_details import ProblemDetails, ProblemDetailsError

from application.controles.queries.consultar_control.dto import ControlRequestDTO
from application.controles.queries.consultar_historico_por_planta.dto import GetHistoricoPorPlantaDTO
from application.controles.queries.consultar_ultimo_control.dto import GetUltimoControlRequestDTO
from application.controles.queries.consultar_ultimo_historico.dto import GetUltimoHistoricoRequestDTO
from application.controles.queries.control_automatico_dataset.dto import ControlAutomaticoDatasetRequestDTO
from application.controles.queries.get_historico.dto import GetHistoricoDTO
from application.controles_planta.alerta_control_por_id_planta.dto import AlertaControlRequestDTO
from application.controles_planta.consultar_control_por_id_planta.dto import ControlByIdRequestDTO
from application.controles_planta.consultar_historico_por_id_planta.dto import GetHistoricoByPlantaIdDTO
from application.controles_planta.consultar_ultimo_control_por_id_planta.dto import GetUltimoControlByPlantaIdDTO
from application.controles_planta.consultar_ultimo_historico_por_id_planta.dto import GetUltimoHistoricoByPlantaIdRequestDTO
from application.controles_planta.control_automatico_dataset_por_id_planta.dto import ControlAutomaticoDatasetByIdRequestDTO

control_planta_bp = Blueprint('control_planta', __name__)

@control_planta_bp.route('/control-por-id-planta', methods=['POST'])
def control_por_id():
    try:
        data = request.json
        dto = ControlByIdRequestDTO(
            idPlanta=data["idPlanta"],
            temperatura=data["temperatura"],
            humedad_aire=data["humedad_aire"],
            humedad_suelo=data["humedad_suelo"]
        )
        result = Mediator.send(dto)
        if "error" in result:
            raise ProblemDetailsError(
                ProblemDetails(
                    status=404,
                    title="Error al consultar control",
                    detail=result["error"]
                )
            )
        return jsonify(result), 200
    except ProblemDetailsError as e:  # <--- ATENCIÓN AQUÍ
        # Propaga el error ProblemDetails tal cual fue lanzado
        raise e
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=500,
                title="Error en la lógica de control por id planta",
                detail=str(e)
            )
        )


    
@control_planta_bp.route('/control-automatico-dataset-por-id-planta', methods=['POST'])
def test_logica():
    try:
        data = request.json
        dto = ControlAutomaticoDatasetByIdRequestDTO(idPlanta=data["idPlanta"])
        result = Mediator.send(dto)
        if "error" in result:
            raise ProblemDetailsError(ProblemDetails(
                status=404,
                title="Tipo de planta desconocido",
                detail=result["error"]
            ))
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(ProblemDetails(
            status=500,
            title="Error en testeo de lógica difusa",
            detail=str(e)
        ))
    
@control_planta_bp.route('/ultimo-control-por-id-planta', methods=['POST'])
def control_ultimo_por_id():
    try:
        data = request.json
        dto = GetUltimoControlByPlantaIdDTO(idPlanta=data["idPlanta"])
        result = Mediator.send(dto)
        if "error" in result:
            raise ProblemDetailsError(
                ProblemDetails(
                    status=404,
                    title="Error al consultar control por histórico",
                    detail=result["error"]
                )
            )
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=500,
                title="Error al consultar último control",
                detail=str(e)
            )
        )

@control_planta_bp.route('/alerta-control-por-id-planta', methods=['POST'])
def alerta_control():
    try:
        data = request.json
        dto = AlertaControlRequestDTO(idPlanta=data["idPlanta"])
        result = Mediator.send(dto)
        return jsonify(result), 200
    except Exception as e:
        from flask_problem_details import ProblemDetails, ProblemDetailsError
        raise ProblemDetailsError(
            ProblemDetails(
                status=500,
                title="Error en alerta de control",
                detail=str(e)
            )
        )


@control_planta_bp.route('/historico-planta', methods=['POST'])
def consultar_historico_by_id():
    try:
        data = request.json
        idPlanta = data['idPlanta']
        dto = GetHistoricoByPlantaIdDTO(idPlanta)
        result = Mediator.send(dto)
        return jsonify([h.__dict__ for h in result]), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Error al consultar histórico por id de planta",
                detail=str(e)
            )
        )


@control_planta_bp.route('/ultimo-historico-planta', methods=['POST'])
def consultar_ultimo_historico_por_id():
    try:
        data = request.json
        idPlanta = data["idPlanta"]
        dto = GetUltimoHistoricoByPlantaIdRequestDTO(idPlanta)
        result = Mediator.send(dto)
        if "error" in result:
            raise ProblemDetailsError(
                ProblemDetails(
                    status=404,
                    title="Histórico no encontrado",
                    detail=result["error"]
                )
            )
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=500,
                title="Error en la consulta",
                detail=str(e)
            )
        )


