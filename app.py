from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "your-email@gmail.com"  # Replace with your email
app.config["MAIL_PASSWORD"] = "your-app-password"  # Replace with your app password

mail = Mail(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_email", methods=["POST"])
def send_email():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    recipient_email = "onecuteaass@gmail.com"  # Default recipient

    # Create and send email
    msg = Message(
        subject="Attached Document",
        sender=app.config["MAIL_USERNAME"],
        recipients=[recipient_email],
        body="Please find the attached document.",
    )
    with app.open_resource(file_path) as fp:
        msg.attach(file.filename, "application/octet-stream", fp.read())

    mail.send(msg)
    return "Email sent successfully!"

if __name__ == "__main__":
    app.run(debug=True)
