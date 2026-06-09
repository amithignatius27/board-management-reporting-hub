from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
from datetime import datetime
import json
from services.json_cleaner import clean_json_response
from services.fallback_service import fallback_description
from services.logger_service import logger
import time

from services.cache_service import (
    get_cached_response,
    save_response_to_cache
)

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/describe", methods=["POST"])
def describe():

    try:
        data = request.get_json()

        # ✅ 1. VALIDATION
        if not data or "input" not in data:
            return jsonify({
                "success": False,
                "error": "Input is required"
            }), 400

        user_input = data["input"]
        user_input = user_input.strip()
        logger.info(f"Describe request received: {user_input}")
        if len(user_input) > 2000:
            return jsonify({
                "success": False,
                "error": "Input too long"
                }), 400

        # ✅ 2. CHECK CACHE
        cached_response = get_cached_response(
            "describe",
            user_input
        )

        if cached_response:
            logger.info("Describe cache hit")
            return jsonify({
                "success": True,
                "source": "cache",
                "data": cached_response
            })

        # ✅ 3. LOAD PROMPT
        with open("prompts/describe.txt", "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.replace("{input}", user_input)
        
        start_time = time.time()

        # ✅ 4. CALL AI
        ai_response = generate_response(prompt)
        end_time = time.time()
        logger.info(f"Describe response time: {end_time - start_time:.2f}s")    

        if ai_response is None:
            logger.warning("Fallback response used")
            return jsonify({
                "success": True,
                "source": "fallback",
                "data": fallback_description()
    })
        

        # ✅ 5. CLEAN RESPONSE
        clean_response = clean_json_response(ai_response)

        # DEBUG (optional)
        print(clean_response)

        # ✅ 6. PARSE JSON
        parsed = json.loads(clean_response)

        # ✅ 7. FINAL RESPONSE DATA
        response_data = {
            "description": parsed.get("description"),
            "insights": parsed.get("insights"),
            "generated_at": datetime.utcnow().isoformat()
        }

        # ✅ 8. SAVE TO CACHE
        save_response_to_cache(
            "describe",
            user_input,
            response_data
        )
        logger.info("Describe AI response generated")

        # ✅ 9. RETURN RESPONSE
        return jsonify({
            "success": True,
            "source": "ai",
            "data": response_data
        })

    except Exception as e:
        logger.error("DESCRIBE ERROR")
        logger.error(str(e))
        return jsonify({
            "success": True,
            "source": "fallback",
            "data": fallback_description()
            })