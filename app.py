from flask import Flask, render_template, request, jsonify
import subprocess
import os
import uuid
import sys
app = Flask(__name__, static_folder="static", static_url_path="/static")
UPLOAD_FOLDER = os.path.join("static", "processed")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/process", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    # Save uploaded file temporarily
    unique_name = f"{uuid.uuid4()}.png"
    input_path = os.path.join(UPLOAD_FOLDER, f"input_{unique_name}")
    output_path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(input_path)
    # Run main.py to process the image
    python_executable = sys.executable
    result = subprocess.run(
        [python_executable, "main.py", input_path, output_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("Error:", result.stderr)
        return jsonify({"error": result.stderr}), 500
    image_url = f"/static/processed/{unique_name}"
    return jsonify({"url": image_url})
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
