from flask import Flask, request, jsonify
import uuid
import pandas as pd
import os
from database import get_db_session
from worker import process_images_task

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    df = pd.read_csv(file_path)

    # Validate CSV format
    required_columns = ["Serial Number", "Product Name", "Input Image Urls"]
    if not all(col in df.columns for col in required_columns):
        return jsonify({"error": "Invalid CSV format"}), 400

    request_id = str(uuid.uuid4())

    session = get_db_session()
    session.execute("INSERT INTO Requests (request_id, status, timestamp) VALUES (:id, :status, GETDATE())",
                    {"id": request_id, "status": "Pending"})
    session.commit()
    session.close()

    process_images_task.delay(request_id, file_path)

    return jsonify({"request_id": request_id}), 202

@app.route("/status/<request_id>", methods=["GET"])
def check_status(request_id):
    session = get_db_session()
    result = session.execute("SELECT status FROM Requests WHERE request_id = :id", {"id": request_id}).fetchone()
    session.close()

    if result:
        return jsonify({"request_id": request_id, "status": result[0]})
    else:
        return jsonify({"error": "Invalid request ID"}), 404

if __name__ == "__main__":
    app.run(debug=True)
