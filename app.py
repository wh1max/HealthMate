
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables from .env file before anything else
load_dotenv()

from utils.ai_logic import analyze_symptoms, generate_summary
from utils.email_handler import send_email

app = Flask(__name__)
CORS(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'false').lower() in ['true', '1', 't']
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'true').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    symptoms_text = data.get('symptoms')
    
    if not symptoms_text:
        return jsonify({'error': 'No symptoms provided'}), 400

    # Simulate AI analysis
    analysis = analyze_symptoms(symptoms_text)
    
    return jsonify(analysis)

@app.route('/summary', methods=['POST'])
def summary():
    data = request.get_json()
    symptoms = data.get('symptoms')
    questions = data.get('questions')
    answers = data.get('answers')
    email = data.get('email')

    if not all([symptoms, questions, answers, email]):
        return jsonify({'error': 'Missing data for summary'}), 400

    # Generate health summary
    summary_text = generate_summary(symptoms, questions, answers)
    
    # Send email with the summary
    try:
        send_email(mail, email, symptoms, summary_text)
    except Exception as e:
        # Log the error and potentially inform the user
        print(f"Error sending email: {e}")
        # Decide if this should be a critical failure or not
        # For now, we'll just log it and continue

    return jsonify({'summary': summary_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
