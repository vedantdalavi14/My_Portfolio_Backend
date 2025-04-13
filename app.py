from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('EMAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('EMAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('EMAIL_USERNAME')
)

mail = Mail(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Create HTML email content
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #4F46E5, #7C3AED); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0;">New Contact Form Message</h1>
            </div>
            <div style="background: white; padding: 20px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <div style="margin-bottom: 15px;">
                    <strong style="color: #4F46E5;">Name:</strong>
                    <div>{name}</div>
                </div>
                <div style="margin-bottom: 15px;">
                    <strong style="color: #4F46E5;">Email:</strong>
                    <div>{email}</div>
                </div>
                <div style="margin-bottom: 15px;">
                    <strong style="color: #4F46E5;">Subject:</strong>
                    <div>{subject}</div>
                </div>
                <div style="margin-bottom: 15px;">
                    <strong style="color: #4F46E5;">Message:</strong>
                    <div>{message}</div>
                </div>
            </div>
        </div>
        """

        # Send email
        msg = Message(
            subject=f"New Contact Form Message: {subject}",
            recipients=[os.getenv('RECIPIENT_EMAIL')],
            html=html_content,
            reply_to=email
        )
        mail.send(msg)

        # Send auto-response
        auto_response = Message(
            subject="Thank you for your message",
            recipients=[email],
            html=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #4F46E5, #7C3AED); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0;">Thank You!</h1>
                </div>
                <div style="background: white; padding: 20px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <p>Hello {name},</p>
                    <p>Thank you for reaching out! I have received your message and will get back to you as soon as possible.</p>
                    <p>Best regards,<br>Vedya</p>
                </div>
            </div>
            """
        )
        mail.send(auto_response)

        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 