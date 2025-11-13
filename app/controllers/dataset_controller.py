# app/controllers/csv_dataset_bp.py
from flask import Blueprint, request, jsonify, send_file
from flask_problem_details import ProblemDetails, ProblemDetailsError
from flask_jwt_extended import jwt_required
from mediatr import Mediator

from application.datasets.commands.delete_dataset.dto import DeleteCsvDatasetDTO
from application.datasets.commands.upload_dataset.dto import UploadCsvDatasetDTO
from application.datasets.queries.download_dataset.dto import DownloadCsvDatasetDTO
from application.datasets.queries.listar_datasets.dto import ListCsvDatasetDTO

csv_dataset_bp = Blueprint('csv_dataset', __name__)

@csv_dataset_bp.route('', methods=['POST'])
@jwt_required()
def upload_csv_dataset():
    try:
        file = request.files["file"]
        dto = UploadCsvDatasetDTO(file_storage=file)
        result = Mediator.send(dto)
        return jsonify(result), 201
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=400,
                title="Error al cargar archivo",
                detail=str(e)
            )
        )

@csv_dataset_bp.route('', methods=['GET'])
@jwt_required()
def list_csv_datasets():
    try:
        dto = ListCsvDatasetDTO()
        result = Mediator.send(dto)
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=500,
                title="Error al listar archivos",
                detail=str(e)
            )
        )

@csv_dataset_bp.route('/<filename>', methods=['GET'])
@jwt_required()
def download_csv_dataset(filename):
    try:
        dto = DownloadCsvDatasetDTO(filename)
        path = Mediator.send(dto)
        return send_file(path, mimetype='text/csv', as_attachment=True)
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Archivo no encontrado",
                detail=str(e)
            )
        )

@csv_dataset_bp.route('/<filename>', methods=['DELETE'])
@jwt_required()
def delete_csv_dataset(filename):
    try:
        dto = DeleteCsvDatasetDTO(filename)
        result = Mediator.send(dto)
        return jsonify(result), 200
    except Exception as e:
        raise ProblemDetailsError(
            ProblemDetails(
                status=404,
                title="Error al eliminar archivo",
                detail=str(e)
            )
        )
