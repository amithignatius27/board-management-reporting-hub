from flask import Flask
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
from routes.health import health_bp
from flask_cors import CORS
from flask_talisman import Talisman
from services.embedding_service import embedding_model



app = Flask(__name__)
CORS(app)

Talisman(app)

app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)
app.register_blueprint(health_bp)

@app.route('/health')
def health():
    return {"status": "AI service running"}

@app.route("/")
def home():
    return {"message": "AI Service is running"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)