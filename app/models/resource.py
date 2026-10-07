from datetime import datetime
from app.models.user import db

class DownloadResource(db.Model):
    __tablename__ = 'download_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), default='Syllabus') # Syllabus, Routine, Model Question, Form, Report, Calendar
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.String(30), nullable=True) # e.g. '1.2 MB'
    file_type = db.Column(db.String(20), default='pdf') # pdf, docx, xlsx
    download_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DownloadResource {self.title}>'
