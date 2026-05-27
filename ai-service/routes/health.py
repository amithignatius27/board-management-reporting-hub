from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():

    return jsonify({
        "success": True,
        "service": "ai-service",
        "status": "healthy",
        "model": "llama-3.3-70b-versatile",
        "uptime": "active",
        "avg_response_time": "1.2s",
        "timestamp": datetime.now().isoformat()
    })