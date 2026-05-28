def clean_json_response(response):

    if not response:
        return ""

    return (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )