from datetime import datetime
from app.models.user import db

class GalleryItem(db.Model):
    __tablename__ = 'gallery_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), default='photo') # 'photo' or 'video'
    category = db.Column(db.String(50), default='Events') # Events, Campus, Sports, Celebration, Academic
    media_url = db.Column(db.String(255), nullable=False) # File path or YouTube video URL
    thumbnail_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GalleryItem {self.title} ({self.type})>'
