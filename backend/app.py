#sample flask app structure to integrate with tsx frontend
#run this file using python app.py
#open browser and go to http://localhost:5000/api/data to see the response
#open browser and go to http://localhost:5000/api/feedback to see the response

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])   ##set up this as path for get req http://127.0.0.1:5000/api/data
def get_data():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/feedback', methods=['POST'])  #set up this as path for post req http://127.0.0.1:5000/api/feedback
def receive_feedback():
    feedback = request.json.get('feedback', '')
    return jsonify({"message": "Feedback received", "feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)
