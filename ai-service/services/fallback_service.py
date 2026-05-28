def fallback_description():

    return {
        "description": "AI service temporarily unavailable",
        "insights": "Fallback response generated"
    }


def fallback_recommendations():

    return [
        {
            "action_type": "Monitor",
            "description": "Review business metrics manually",
            "priority": "Medium"
        },
        {
            "action_type": "Escalate",
            "description": "Notify management team",
            "priority": "High"
        },
        {
            "action_type": "Stabilize",
            "description": "Maintain operational continuity",
            "priority": "High"
        }
    ]


def fallback_report():

    return {
        "title": "Fallback Report",
        "summary": "AI report generation unavailable",
        "overview": "Fallback report generated",
        "recommendations": [
            "Retry request later"
        ]
    }