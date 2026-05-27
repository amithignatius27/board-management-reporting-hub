from flask import Flask
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
app = Flask(__name__)

app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)

@app.route('/health')
def health():
    return {"status": "AI service running"}

@app.route("/")
def home():
    return {"message": "AI Service is running"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)