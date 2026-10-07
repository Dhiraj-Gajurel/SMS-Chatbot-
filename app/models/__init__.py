from app.models.user import db, User
from app.models.notice import Notice
from app.models.event import Event
from app.models.gallery import GalleryItem
from app.models.academic import AcademicProgram, Facility, StaffMember
from app.models.resource import DownloadResource
from app.models.inquiry import AdmissionInquiry, ContactMessage
from app.models.settings import SiteSetting, HeroBanner, Testimonial

__all__ = [
    'db',
    'User',
    'Notice',
    'Event',
    'GalleryItem',
    'AcademicProgram',
    'Facility',
    'StaffMember',
    'DownloadResource',
    'AdmissionInquiry',
    'ContactMessage',
    'SiteSetting',
    'HeroBanner',
    'Testimonial'
]
