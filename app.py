import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# Get DATABASE_URL from environment, with your local PostgreSQL as fallback
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:StevenTranBlockHead#PostgreSQL@localhost/website_db')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)  # Fix for SQLAlchemy compatibility

# Set the database URI in Flask config
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Models (based on your original code, expanded as needed)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Session(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    device_type = db.Column(db.String(10))  # 'mobile' or 'laptop'

class SectionView(db.Model):
    __tablename__ = 'section_view'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), db.ForeignKey('session.id'))
    section = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), db.ForeignKey('session.id'))
    section = db.Column(db.String(50))
    element = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables in the database
with app.app_context():
    db.create_all()

# Routes (from your original code)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/submit-message', methods=['POST'])
def submit_message():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400
    new_message = Message(name=name, email=email, message=message)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message received successfully"}), 201

@app.route('/api/log-page-view', methods=['POST'])
def log_page_view():
    data = request.get_json()
    session_id = data['session_id']
    device_type = data['device_type']
    existing_session = Session.query.get(session_id)
    if not existing_session:
        session = Session(id=session_id, device_type=device_type)
        db.session.add(session)
        db.session.commit()
    return {'status': 'success'}

@app.route('/api/log-section-view', methods=['POST'])
def log_section_view():
    data = request.get_json()
    session_id = data['session_id']
    section = data['section']
    view = SectionView(session_id=session_id, section=section)
    db.session.add(view)
    db.session.commit()
    return {'status': 'success'}

@app.route('/api/log-click', methods=['POST'])
def log_click():
    data = request.get_json()
    session_id = data['session_id']
    section = data['section']
    element = data['element']
    click = Click(session_id=session_id, section=section, element=element)
    db.session.add(click)
    db.session.commit()
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
