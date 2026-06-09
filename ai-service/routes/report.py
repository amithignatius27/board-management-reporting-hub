from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
from datetime import datetime
import json
import time

from services.json_cleaner import clean_json_response
from services.fallback_service import fallback_report
from services.logger_service import logger

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

        user_input = user_input.strip()

        if not user_input:
            return jsonify({
                "success": False,
                "error": "Empty input not allowed"
            }), 400

        logger.info(
            f"Report request received: {user_input}"
        )

        if len(user_input) > 2000:
            return jsonify({
                "success": False,
                "error": "Input too long"
            }), 400

        # ✅ CHECK CACHE
        cached_response = get_cached_response(
            "generate-report",
            user_input
        )

        if cached_response:

            logger.info(
                "Report cache hit"
            )

            return jsonify({
                "success": True,
                "source": "cache",
                "data": cached_response
            })

        # load prompt
        with open("prompts/report.txt", "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.replace(
            "{{input}}",
            user_input
        )

        start_time = time.time()

        # call AI
        response = generate_response(prompt)

        end_time = time.time()

        logger.info(
            f"Report response time: {end_time - start_time:.2f}s"
        )

        if response is None:

            logger.warning(
                "Report fallback response used"
            )

            return jsonify({
                "success": True,
                "source": "fallback",
                "data": fallback_report()
            })

        # clean markdown formatting
        clean_response = clean_json_response(
            response
        )

        print("AI RAW RESPONSE:")
        print(clean_response)

        # convert AI response to JSON
        report_data = json.loads(
            clean_response
        )

        # ✅ SAVE TO CACHE
        save_response_to_cache(
            "generate-report",
            user_input,
            report_data
        )

        logger.info(
            "Report AI response generated"
        )

        # final structured response
        return jsonify({
            "success": True,
            "source": "ai",
            "data": report_data,
            "generated_at": datetime.now().isoformat()
        })

    except Exception as e:

        logger.error(
            "REPORT ERROR"
        )

        logger.error(
            str(e)
        )

        return jsonify({
            "success": True,
            "source": "fallback",
            "data": fallback_report()
        })