from datetime import datetime
from app.models.user import db

class AdmissionInquiry(db.Model):
    __tablename__ = 'admission_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150), nullable=False)
    guardian_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    grade_applying = db.Column(db.String(30), nullable=False) # Nursery, Class 1-10, +2 Management, Technical
    previous_school = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='Pending') # Pending, Contacted, Admitted, Rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
