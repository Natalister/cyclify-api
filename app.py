from flask import Flask, jsonify
from scraper import get_upcoming_races

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "Cycling API is running"})

@app.route('/races')
def races():
    data = get_upcoming_races()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
