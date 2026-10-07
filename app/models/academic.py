from datetime import datetime
from app.models.user import db

class AcademicProgram(db.Model):
    __tablename__ = 'academic_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(100), nullable=False) # e.g. Pre-Primary, Basic Level (1-8), Secondary (+2 Management / Technical)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='fa-graduation-cap')
    order = db.Column(db.Integer, default=0)

class Facility(db.Model):
    __tablename__ = 'facilities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='fa-school')
    image = db.Column(db.String(255), nullable=True)

class StaffMember(db.Model):
    __tablename__ = 'staff_members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    designation = db.Column(db.String(100), nullable=False) # e.g. Principal, Vice Principal, Head of Department, Senior Teacher, SMC Member, PTA Member
    type = db.Column(db.String(30), default='Teacher') # Teacher, SMC, PTA, Administration
    qualification = db.Column(db.String(150), nullable=True)
    photo = db.Column(db.String(255), default='default_staff.png')
    phone = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
