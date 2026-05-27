from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
from datetime import datetime
import json

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

        # load prompt
        with open("prompts/report.txt", "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.replace("{{input}}", user_input)

        # call AI
        response = generate_response(prompt)

        # convert AI response to JSON
        clean_response = response.replace("```json", "").replace("```", "").strip()
        print("AI RAW RESPONSE:")
        print(clean_response)
        report_data = json.loads(clean_response)
        

        # final structured response
        return jsonify({
            "success": True,
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