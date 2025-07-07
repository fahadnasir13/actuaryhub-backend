from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///jobs.db')
# Handle PostgreSQL URL format for SQLAlchemy
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CORS configuration for production
CORS(app, origins=[
    "http://localhost:5173",  # Development
    "https://*.vercel.app",   # Vercel deployments
    "https://actuaryhub.vercel.app"  # Production domain
])

# Job Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    posting_date = db.Column(db.Date, nullable=False, default=date.today)
    job_type = db.Column(db.String(50), nullable=False, default='Full-time')
    tags = db.Column(db.Text)  # JSON string of tags
    description = db.Column(db.Text)
    salary = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'posting_date': self.posting_date.isoformat() if self.posting_date else None,
            'job_type': self.job_type,
            'tags': eval(self.tags) if self.tags else [],
            'description': self.description,
            'salary': self.salary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        # Get query parameters
        job_type = request.args.get('job_type')
        location = request.args.get('location')
        keyword = request.args.get('keyword')
        sort = request.args.get('sort', 'posting_date_desc')
        
        # Build query
        query = Job.query
        
        # Apply filters
        if job_type:
            query = query.filter(Job.job_type == job_type)
        
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        
        if keyword:
            query = query.filter(
                db.or_(
                    Job.title.ilike(f'%{keyword}%'),
                    Job.company.ilike(f'%{keyword}%'),
                    Job.tags.ilike(f'%{keyword}%')
                )
            )
        
        # Apply sorting
        if sort == 'posting_date_desc':
            query = query.order_by(Job.posting_date.desc())
        elif sort == 'posting_date_asc':
            query = query.order_by(Job.posting_date.asc())
        elif sort == 'title_asc':
            query = query.order_by(Job.title.asc())
        elif sort == 'title_desc':
            query = query.order_by(Job.title.desc())
        
        jobs = query.all()
        return jsonify([job.to_dict() for job in jobs])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = Job.query.get_or_404(job_id)
        return jsonify(job.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/jobs', methods=['POST'])
def create_job():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['title', 'company', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new job
        job = Job(
            title=data['title'],
            company=data['company'],
            location=data['location'],
            posting_date=datetime.strptime(data.get('posting_date', date.today().isoformat()), '%Y-%m-%d').date(),
            job_type=data.get('job_type', 'Full-time'),
            tags=str(data.get('tags', [])),
            description=data.get('description'),
            salary=data.get('salary')
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify(job.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        job = Job.query.get_or_404(job_id)
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            job.title = data['title']
        if 'company' in data:
            job.company = data['company']
        if 'location' in data:
            job.location = data['location']
        if 'posting_date' in data:
            job.posting_date = datetime.strptime(data['posting_date'], '%Y-%m-%d').date()
        if 'job_type' in data:
            job.job_type = data['job_type']
        if 'tags' in data:
            job.tags = str(data['tags'])
        if 'description' in data:
            job.description = data['description']
        if 'salary' in data:
            job.salary = data['salary']
        
        job.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(job.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        job = Job.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.utcnow().isoformat(),
        'version': '2.0.0',
        'environment': os.getenv('FLASK_ENV', 'development')
    })

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'ActuaryHub API v2.0',
        'status': 'running',
        'endpoints': {
            'jobs': '/api/jobs',
            'health': '/api/health'
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)