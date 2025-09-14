from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os
import re
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internship_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    aadhar_verified = db.Column(db.Boolean, default=False)
    aadhar_number = db.Column(db.String(12), nullable=True)
    education_level = db.Column(db.String(50), nullable=False)
    field_of_study = db.Column(db.String(100), nullable=False)
    university = db.Column(db.String(200), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.Text, nullable=True)
    resume_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    company_type = db.Column(db.String(50), nullable=False)  # 'trust', 'government', 'private'
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    stipend = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    application_deadline = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    skills_required = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    cover_letter = db.Column(db.Text, nullable=True)

# Helper Functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def load_sample_data():
    """Load sample internship data from JSON file"""
    try:
        with open('data/internships.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []

def populate_database():
    """Populate database with sample internship data"""
    sample_data = load_sample_data()
    
    for internship_data in sample_data:
        # Check if internship already exists
        existing = Internship.query.filter_by(
            title=internship_data['title'],
            company=internship_data['company']
        ).first()
        
        if not existing:
            internship = Internship(
                title=internship_data['title'],
                company=internship_data['company'],
                company_type=internship_data['company_type'],
                description=internship_data['description'],
                requirements=internship_data['requirements'],
                duration=internship_data['duration'],
                stipend=internship_data.get('stipend', 'Unpaid'),
                location=internship_data['location'],
                start_date=datetime.strptime(internship_data['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(internship_data['end_date'], '%Y-%m-%d').date(),
                application_deadline=datetime.strptime(internship_data['application_deadline'], '%Y-%m-%d').date(),
                category=internship_data['category'],
                skills_required=internship_data.get('skills_required', ''),
                is_verified=True
            )
            db.session.add(internship)
    
    db.session.commit()

# Routes
@app.route('/')
def index():
    """Home page with featured internships"""
    featured_internships = Internship.query.filter_by(is_verified=True).limit(6).all()
    return render_template('index.html', internships=featured_internships)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash('User not found. Please create a profile first.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        education_level = request.form['education_level']
        field_of_study = request.form['field_of_study']
        university = request.form['university']
        graduation_year = int(request.form['graduation_year'])
        skills = request.form.get('skills', '')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login instead.', 'error')
            return redirect(url_for('login'))
        
        # Create new user
        user = User(
            name=name,
            email=email,
            mobile=mobile,
            education_level=education_level,
            field_of_study=field_of_study,
            university=university,
            graduation_year=graduation_year,
            skills=skills
        )
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        session['user_name'] = user.name
        
        flash('Profile created successfully! Please verify your Aadhar for full access.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user = User.query.get(session['user_id'])
    recent_applications = Application.query.filter_by(user_id=user.id).order_by(Application.applied_at.desc()).limit(5).all()
    
    # Get recommended internships based on user's field of study
    recommended = Internship.query.filter(
        Internship.category.contains(user.field_of_study),
        Internship.is_verified == True
    ).limit(6).all()
    
    return render_template('dashboard.html', user=user, applications=recent_applications, recommended=recommended)

@app.route('/internships')
def internships():
    """Browse all internships with filters"""
    page = request.args.get('page', 1, type=int)
    company_type = request.args.get('company_type', 'all')
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = Internship.query.filter_by(is_verified=True)
    
    if company_type != 'all':
        query = query.filter_by(company_type=company_type)
    
    if category != 'all':
        query = query.filter(Internship.category.contains(category))
    
    if search:
        query = query.filter(
            db.or_(
                Internship.title.contains(search),
                Internship.company.contains(search),
                Internship.description.contains(search)
            )
        )
    
    internships = query.order_by(Internship.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('internships.html', internships=internships, 
                         company_type=company_type, category=category, search=search)

@app.route('/internship/<int:internship_id>')
def internship_detail(internship_id):
    """Individual internship detail page"""
    internship = Internship.query.get_or_404(internship_id)
    user_applied = False
    
    if 'user_id' in session:
        application = Application.query.filter_by(
            user_id=session['user_id'],
            internship_id=internship_id
        ).first()
        user_applied = application is not None
    
    # Pass current date to template
    today = datetime.now().date()
    
    return render_template('internship_detail.html', internship=internship, user_applied=user_applied, today=today)

@app.route('/apply/<int:internship_id>', methods=['POST'])
@login_required
def apply_internship(internship_id):
    """Apply for an internship"""
    user = User.query.get(session['user_id'])
    internship = Internship.query.get_or_404(internship_id)
    
    # Check if already applied
    existing_application = Application.query.filter_by(
        user_id=user.id,
        internship_id=internship_id
    ).first()
    
    if existing_application:
        flash('You have already applied for this internship.', 'warning')
        return redirect(url_for('internship_detail', internship_id=internship_id))
    
    # Check if application deadline has passed
    if datetime.now().date() > internship.application_deadline:
        flash('Application deadline has passed for this internship.', 'error')
        return redirect(url_for('internship_detail', internship_id=internship_id))
    
    cover_letter = request.form.get('cover_letter', '')
    
    application = Application(
        user_id=user.id,
        internship_id=internship_id,
        cover_letter=cover_letter
    )
    
    db.session.add(application)
    db.session.commit()
    
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('internship_detail', internship_id=internship_id))

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    user = User.query.get(session['user_id'])
    
    user.name = request.form['name']
    user.mobile = request.form['mobile']
    user.education_level = request.form['education_level']
    user.field_of_study = request.form['field_of_study']
    user.university = request.form['university']
    user.graduation_year = int(request.form['graduation_year'])
    user.skills = request.form.get('skills', '')
    
    db.session.commit()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/verify_aadhar', methods=['POST'])
@login_required
def verify_aadhar():
    """Verify Aadhar using DigiLocker integration (simulated)"""
    user = User.query.get(session['user_id'])
    aadhar_number = request.form['aadhar_number']
    
    # Simulate Aadhar verification
    if len(aadhar_number) == 12 and aadhar_number.isdigit():
        user.aadhar_number = aadhar_number
        user.aadhar_verified = True
        user.is_verified = True
        db.session.commit()
        flash('Aadhar verified successfully!', 'success')
    else:
        flash('Invalid Aadhar number. Please check and try again.', 'error')
    
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))

# API Routes
@app.route('/api/internships')
def api_internships():
    """API endpoint for internships data"""
    internships = Internship.query.filter_by(is_verified=True).all()
    return jsonify([{
        'id': i.id,
        'title': i.title,
        'company': i.company,
        'company_type': i.company_type,
        'location': i.location,
        'duration': i.duration,
        'stipend': i.stipend,
        'start_date': i.start_date.isoformat(),
        'end_date': i.end_date.isoformat(),
        'application_deadline': i.application_deadline.isoformat(),
        'category': i.category
    } for i in internships])

@app.route('/api/stats')
def api_stats():
    """API endpoint for platform statistics"""
    total_internships = Internship.query.filter_by(is_verified=True).count()
    trust_internships = Internship.query.filter_by(company_type='trust', is_verified=True).count()
    government_internships = Internship.query.filter_by(company_type='government', is_verified=True).count()
    private_internships = Internship.query.filter_by(company_type='private', is_verified=True).count()
    
    return jsonify({
        'total_internships': total_internships,
        'trust_internships': trust_internships,
        'government_internships': government_internships,
        'private_internships': private_internships
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_database()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
