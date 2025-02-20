from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

@app.route("/")
def home():
    return render_template("index.html")  # Load the HTML page

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file selected", 400

    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Generate a file URL to attach in Gmail
    file_url = request.host_url + "download/" + file.filename

    # Get recipient email
    recipient = request.form.get("recipient", "")

    # Gmail Intent (works on Android)
    gmail_intent = f"mailto:{recipient}?subject=Attached%20Document&body=Please%20find%20the%20attached%20file.%0A{file_url}"

    return redirect(gmail_intent)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)

