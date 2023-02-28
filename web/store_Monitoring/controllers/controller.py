# from helpers import generate_report_id, get_store_business_hours, get_store_timezone, \
#                     get_store_uptime_downtime, generate_report_csv

from flask import Blueprint, request, jsonify
import asyncio
from store_Monitoring import database
from store_Monitoring.helpers.auth import is_authenticated
from store_Monitoring.tasks import create_task
# from project.models.project import Project

from celery.result import AsyncResult
blueprint = Blueprint("store_Monitoring_bp", __name__)


@blueprint.route('/trigger_report', methods=['GET'])
# @is_authenticated
def trigger_report():
    # content = request.json
    # task_type = content["type"]
    task = create_task.delay(10)
    return jsonify({"task_id": task.id}), 202

@blueprint.route('/get_report/<task_id>', methods=['GET'])
# @is_authenticated
def get_report(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200

