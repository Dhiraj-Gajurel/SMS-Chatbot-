from datetime import datetime
from app.models.user import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(150), default='School Ground / Auditorium')
    category = db.Column(db.String(50), default='Academic') # Academic, Sports, Cultural, Holiday, Exam
    image = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.title}>'
