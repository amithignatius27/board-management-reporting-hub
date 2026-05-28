from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
import json
from services.json_cleaner import clean_json_response

from services.cache_service import (
    get_cached_response,
    save_response_to_cache
)

recommend_bp = Blueprint("recommend", __name__)


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():

    try:
        data = request.get_json()

        # validation
        if not data or "input" not in data:
            return jsonify({
                "success": False,
                "error": "Input is required"
            }), 400

        user_input = data["input"]
        if len(user_input) > 2000:
            return jsonify({
                "success": False,
                "error": "Input too long"
                }), 400

        # load prompt
        with open("prompts/recommend.txt", "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.replace("{input}", user_input)

        # check cache
        cached_response = get_cached_response(
            "recommend",
            user_input
        )

        if cached_response:
            return jsonify({
                "success": True,
                "source": "cache",
                "data": cached_response
            })

        # call AI
        ai_response = generate_response(prompt)

        if ai_response is None:
            return jsonify({
                "success": False,
                "error": "AI service failed"
            }), 500

        # clean markdown
        clean_response = clean_json_response(ai_response)

        # parse JSON
        recommendations = json.loads(clean_response)

        # validate exactly 3 items
        if not isinstance(recommendations, list) or len(recommendations) != 3:
            return jsonify({
                "success": False,
                "error": "AI did not return exactly 3 recommendations"
            }), 500

        # save to cache
        save_response_to_cache(
            "recommend",
            user_input,
            recommendations
        )

        return jsonify({
            "success": True,
            "source": "ai",
            "data": recommendations
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "is_fallback": True,
            "error": "Recommendation generation failed",
            "details": str(e)
        }), 500