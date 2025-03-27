#sample flask app structure to integrate with tsx frontend
#run this file using python app.py
#open browser and go to http://localhost:5000/api/data to see the response
#open browser and go to http://localhost:5000/api/feedback to see the response

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
# from deepfake_detector import analyze_audio  # Your deepfake detection logic
# from audio_recorder import record_audio  # Function to record audio

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
REPORTS_FOLDER = "reports"

REPORTS_FOLDER = "reports"  #downloaded reports will be stored here
REPORT_FILE = os.path.join(REPORTS_FOLDER, "live_recording.json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

@app.route('/api/data', methods=['GET'])   ##set up this as path for get req http://127.0.0.1:5000/api/data
def get_data():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/feedback', methods=['POST'])  #set up this as path for post req http://127.0.0.1:5000/api/feedback
def receive_feedback():
    data = request.json
    feedback_type = data.get('feedbackType')
    message = data.get('message')
    rating = data.get('rating')

    print(f"Received feedback: Type={feedback_type}, Message={message}, Rating={rating}")

    return jsonify({"message": "Feedback received successfully"}), 200

# 1. Endpoint to analyze an uploaded audio file
@app.route('/analyze-audio', methods=['POST'])
def analyze_audio_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # results = analyze_audio(filepath)  # Your deepfake detection function

    # Save results as a report
    # report_path = os.path.join(REPORTS_FOLDER, f"{file.filename}.json")
    # with open(report_path, "w") as f:
    #     f.write(json.dumps(results))

    # return jsonify(results)

# 2. Endpoint to record and analyze live audio
# @app.route('/record-audio', methods=['POST'])
# def record_audio_file():
    # audio_path = record_audio()  # Your function to capture audio from the microphone

    # results = analyze_audio(audio_path)
    # report_path = os.path.join(REPORTS_FOLDER, "live_recording.json")
    # with open(report_path, "w") as f:
    #     f.write(json.dumps(results))

    # return jsonify(results)

# 3. Endpoint to download analysis reports
@app.route('/download-report', methods=['GET'])
def download_report():
    filename = request.args.get("filename")
    
    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    # Prevent directory traversal attacks
    safe_filename = os.path.basename(filename)
    report_path = os.path.join(REPORTS_FOLDER, safe_filename)

    if not os.path.exists(report_path):
        return jsonify({"error": "Report not found"}), 404

    return send_file(report_path, as_attachment=True, download_name=safe_filename)

if __name__ == '__main__':
    app.run(debug=True)
