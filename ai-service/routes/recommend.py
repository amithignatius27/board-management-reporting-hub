from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
import json

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    # ✅ validation
    if not data or "input" not in data:
        return jsonify({"error": "Input is required"}), 400

    user_input = data["input"]

    # ✅ load prompt
    with open("prompts/recommend.txt", "r") as f:
        prompt_template = f.read()

    prompt = prompt_template.replace("{input}", user_input)

    # ✅ call AI
    ai_response = generate_response(prompt)

    if ai_response is None:
        return jsonify({"error": "AI service failed"}), 500

    # ✅ parse JSON
    try:
        parsed = json.loads(ai_response)

        # 🔥 enforce exactly 3 recommendations
        if not isinstance(parsed, list) or len(parsed) != 3:
            return jsonify({"error": "AI did not return exactly 3 recommendations"}), 500

    except Exception as e:
        return jsonify({"error": "Invalid AI response"}), 500

    return jsonify(parsed)