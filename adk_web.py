"""
ADK Web Command Representation - Flask Web App
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "ADK Web berjalan di Cloud Run!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
