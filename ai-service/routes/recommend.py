from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
import json
import time

from services.json_cleaner import clean_json_response
from services.fallback_service import fallback_recommendations
from services.logger_service import logger

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

        user_input = user_input.strip()

        if not user_input:
            return jsonify({
                "success": False,
                "error": "Empty input not allowed"
            }), 400

        logger.info(
            f"Recommend request received: {user_input}"
        )

        if len(user_input) > 2000:
            return jsonify({
                "success": False,
                "error": "Input too long"
            }), 400

        # load prompt
        with open("prompts/recommend.txt", "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.replace(
            "{input}",
            user_input
        )

        # check cache
        cached_response = get_cached_response(
            "recommend",
            user_input
        )

        if cached_response:

            logger.info(
                "Recommend cache hit"
            )

            return jsonify({
                "success": True,
                "source": "cache",
                "data": cached_response
            })

        start_time = time.time()

        # call AI
        ai_response = generate_response(prompt)

        end_time = time.time()

        logger.info(
            f"Recommend response time: {end_time - start_time:.2f}s"
        )

        if ai_response is None:

            logger.warning(
                "Recommend fallback response used"
            )

            return jsonify({
                "success": True,
                "source": "fallback",
                "data": fallback_recommendations()
            })

        # clean markdown
        clean_response = clean_json_response(
            ai_response
        )

        # parse JSON
        recommendations = json.loads(
            clean_response
        )

        # validate exactly 3 items
        if not isinstance(recommendations, list) or len(recommendations) != 3:

            logger.warning(
                "AI did not return exactly 3 recommendations"
            )

            return jsonify({
                "success": True,
                "source": "fallback",
                "data": fallback_recommendations()
            })

        # save to cache
        save_response_to_cache(
            "recommend",
            user_input,
            recommendations
        )

        logger.info(
            "Recommend AI response generated"
        )

        return jsonify({
            "success": True,
            "source": "ai",
            "data": recommendations
        })

    except Exception as e:

        logger.error(
            "RECOMMEND ERROR"
        )

        logger.error(
            str(e)
        )

        return jsonify({
            "success": True,
            "source": "fallback",
            "data": fallback_recommendations()
        })