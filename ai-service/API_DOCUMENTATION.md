# AI Service API Documentation

## Base URL

http://127.0.0.1:5000

---

## 1. Describe

POST /describe

Request:

{
    "input": "Revenue dropped due to supply chain issues"
}

Response:

{
    "success": true,
    "source": "ai",
    "data": {
        "description": "...",
        "insights": "..."
    }
}

---

## 2. Recommend

POST /recommend

Request:

{
    "input": "Revenue dropped due to supply chain issues"
}

Response:

{
    "success": true,
    "source": "ai",
    "data": [...]
}

---

## 3. Generate Report

POST /generate-report

Request:

{
    "input": "Revenue dropped due to supply chain issues"
}

Response:

{
    "success": true,
    "source": "ai",
    "data": {...}
}

---

## 4. Health Check

GET /health

Response:

{
    "status": "healthy"
}