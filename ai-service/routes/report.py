from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
from datetime import datetime
import json

from services.cache_service import (
    get_cached_response,
    save_response_to_cache
)

report_bp = Blueprint("report", __name__)

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():

    try:
        data = request.get_json()

        # validation
        if not data or "input" not in data:
            return jsonify({
                "success": False,
                "error": "Input is required"
            }), 400

        user_input = data["input"]

        # ✅ CHECK CACHE
        cached_response = get_cached_response(
            "generate-report",
            user_input
        )

        if cached_response:
            return jsonify({
                "success": True,
                "source": "cache",
                "data": cached_response
            })

        # load prompt
        with open("prompts/report.txt", "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.replace("{{input}}", user_input)

        # call AI
        response = generate_response(prompt)

        if response is None:
            return jsonify({
                "success": False,
                "error": "AI service failed"
            }), 500

        # clean markdown formatting
        clean_response = response.replace(
            "```json", ""
        ).replace(
            "```", ""
        ).strip()

        print("AI RAW RESPONSE:")
        print(clean_response)

        # convert AI response to JSON
        report_data = json.loads(clean_response)

        # ✅ SAVE TO CACHE
        save_response_to_cache(
            "generate-report",
            user_input,
            report_data
        )

        # final structured response
        return jsonify({
            "success": True,
            "source": "ai",
            "data": report_data,
            "generated_at": datetime.now().isoformat()
        })

    except Exception as e:

        # fallback response
        return jsonify({
            "success": False,
            "is_fallback": True,
            "error": "AI report generation failed",
            "details": str(e)
        }), 500