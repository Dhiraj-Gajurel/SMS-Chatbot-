from datetime import datetime
from app.models.user import db

class Notice(db.Model):
    __tablename__ = 'notices'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(50), default='General') # General, Vacancy, Exam, Quotation, Admission, Result
    content = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255), nullable=True) # PDF or image attachment
    is_urgent = db.Column(db.Boolean, default=False)
    published_date = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    author = db.relationship('User', backref=db.backref('notices', lazy=True))

    def __repr__(self):
        return f'<Notice {self.title}>'
