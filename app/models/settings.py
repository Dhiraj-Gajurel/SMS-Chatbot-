from datetime import datetime
from app.models.user import db

class SiteSetting(db.Model):
    __tablename__ = 'site_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)

    @classmethod
    def get_val(cls, key, default=''):
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default

    @classmethod
    def set_val(cls, key, value):
        setting = cls.query.filter_by(key=key).first()
        if not setting:
            setting = cls(key=key, value=value)
            db.session.add(setting)
        else:
            setting.value = value
        db.session.commit()

class HeroBanner(db.Model):
    __tablename__ = 'hero_banners'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=False)
    button_text = db.Column(db.String(50), nullable=True)
    button_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100), nullable=False) # Alumni, Parent, SEE Topper, Student
    quote = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    grade_batch = db.Column(db.String(50), nullable=True) # e.g. SEE Batch 2080 (GPA 3.95)
    order = db.Column(db.Integer, default=0)
