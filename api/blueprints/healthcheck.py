from flask import Blueprint, jsonify

healthcheck_bp = Blueprint('healthcheck_bp', __name__)

@healthcheck_bp.route('/health')
def healthcheck():
    return jsonify({'health': 'true'})