#sample flask app structure to integrate with tsx frontend
#run this file using python app.py
#open browser and go to http://localhost:5000/api/data to see the response
#open browser and go to http://localhost:5000/api/feedback to see the response

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import threading
import json
import wave
import sounddevice as sd
import smtplib
from email.message import EmailMessage
import numpy as np
# from deepfake_detector import analyze_audio  # Your deepfake detection logic
# from audio_recorder import record_audio  # Function to record audio

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

UPLOAD_FOLDER = "uploads"
REPORTS_FOLDER = "reports"

REPORT_FILE = os.path.join(REPORTS_FOLDER, "live_recording.json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

recording = []
recording_active = False
samplerate = 44100
channels = 1
stream = None

def callback(indata, frames, time, status):
    """ Callback function to continuously capture audio """
    global recording
    if recording_active:
        recording.append(indata.copy())

# Apply CORS headers to every response
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5174"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

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

# 4. Dummy function to analyze audio
def analyze_audio(filepath):
    return {"status": "success", "message": "Audio analyzed successfully!", "file": filepath}

# 1. Endpoint to analyze an uploaded audio file
@app.route('/analyze-audio', methods=['POST'])
def analyze_audio_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    results = analyze_audio(filepath)  # Your deepfake detection function

    # Save results as a report
    report_path = os.path.join(REPORTS_FOLDER, f"{file.filename}.json")
    with open(report_path, "w") as f:
        f.write(json.dumps(results))

    return jsonify(results)

# 2. Endpoint to record and analyze live audio
@app.route('/record-audio', methods=['POST'])
def start_recording():
    """ Start recording indefinitely """
    global recording, recording_active, stream
    if recording_active:
        return jsonify({"message": "Recording already in progress"}), 400

    recording = []  # Clear previous recording
    recording_active = True

    stream = sd.InputStream(callback=callback, channels=channels, samplerate=samplerate)
    stream.start()

    print("Recording started...")
    return jsonify({"message": "Recording started"}), 200

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    """ Stop recording and save the file """
    global recording_active, stream
    if not recording_active:
        return jsonify({"message": "No recording in progress"}), 400

    recording_active = False
    stream.stop()
    stream.close()

    if not recording:
        return jsonify({"message": "No audio recorded"}), 400

    # Convert recorded audio to NumPy array
    audio_data = np.concatenate(recording, axis=0)
    filepath = os.path.join(UPLOAD_FOLDER, "recorded_audio.wav")

    # Save the recorded audio
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.astype(np.int16).tobytes())

    print(f"Recording saved: {filepath}")
    return jsonify({"message": "Recording stopped", "file_path": filepath}), 200

# 7. Handle CORS preflight requests
@app.route('/record-audio', methods=['OPTIONS'])
def preflight():
    response = jsonify({"message": "CORS preflight successful"})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5174")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

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

@app.route("/share-report", methods=["POST"])
def share_report():
    data = request.json
    method = data.get("method")
    recipient = data.get("recipient")
    
    if not method or not recipient:
        return jsonify({"error": "Invalid request"}), 400
    
    report_path = "reports/analysis_report.pdf"  # Ensure report is saved here

    if method == "email":
        try:
            email_sender = "your-email@gmail.com"
            email_password = "your-email-password"

            msg = EmailMessage()
            msg["Subject"] = "Voice Analysis Report"
            msg["From"] = email_sender
            msg["To"] = recipient
            msg.set_content("Attached is your requested voice analysis report.")

            with open(report_path, "rb") as file:
                msg.add_attachment(file.read(), maintype="application", subtype="pdf", filename="analysis_report.pdf")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(email_sender, email_password)
                server.send_message(msg)

            return jsonify({"message": "Report shared via email successfully!"})

        except Exception as e:
            return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

    elif method == "whatsapp":
        whatsapp_link = f"https://api.whatsapp.com/send?phone={recipient}&text=Your%20analysis%20report%20is%20ready!%20Download%20it%20here:%20http://localhost:5000/download-report"
        return jsonify({"message": "WhatsApp link generated", "link": whatsapp_link})

    return jsonify({"error": "Invalid method"}), 400

if __name__ == '__main__':
    app.run(debug=True)
