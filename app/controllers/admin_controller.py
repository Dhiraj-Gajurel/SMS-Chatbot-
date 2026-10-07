import os
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import (
    db, User, Notice, Event, GalleryItem, AcademicProgram,
    Facility, StaffMember, DownloadResource, AdmissionInquiry,
    ContactMessage, SiteSetting, HeroBanner, Testimonial
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access privileges required.', 'danger')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    notice_count = Notice.query.count()
    event_count = Event.query.count()
    gallery_count = GalleryItem.query.count()
    inquiry_count = AdmissionInquiry.query.count()
    pending_inquiries = AdmissionInquiry.query.filter_by(status='Pending').count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    recent_inquiries = AdmissionInquiry.query.order_by(AdmissionInquiry.created_at.desc()).limit(5).all()
    recent_notices = Notice.query.order_by(Notice.published_date.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        notice_count=notice_count,
        event_count=event_count,
        gallery_count=gallery_count,
        inquiry_count=inquiry_count,
        pending_inquiries=pending_inquiries,
        unread_messages=unread_messages,
        recent_inquiries=recent_inquiries,
        recent_notices=recent_notices
    )

# --- NOTICES MANAGEMENT ---
@admin_bp.route('/notices')
@login_required
@admin_required
def notices():
    notices_list = Notice.query.order_by(Notice.published_date.desc()).all()
    return render_template('admin/notices.html', notices=notices_list)

@admin_bp.route('/notices/add', methods=['POST'])
@login_required
@admin_required
def add_notice():
    title = request.form.get('title')
    category = request.form.get('category', 'General')
    content = request.form.get('content')
    is_urgent = 'is_urgent' in request.form

    if not title or not content:
        flash('Notice title and content are required.', 'danger')
        return redirect(url_for('admin.notices'))

    # Slug creation
    slug = title.lower().replace(' ', '-').replace('/', '-')[:100]
    existing = Notice.query.filter_by(slug=slug).first()
    if existing:
        slug = f"{slug}-{int(datetime.utcnow().timestamp())}"

    attachment_filename = None
    if 'attachment' in request.files:
        file = request.files['attachment']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            attachment_filename = filename

    notice = Notice(
        title=title,
        slug=slug,
        category=category,
        content=content,
        attachment=attachment_filename,
        is_urgent=is_urgent,
        author_id=current_user.id
    )
    db.session.add(notice)
    db.session.commit()
    flash('Notice published successfully!', 'success')
    return redirect(url_for('admin.notices'))

@admin_bp.route('/notices/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_notice(id):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    flash('Notice deleted successfully.', 'info')
    return redirect(url_for('admin.notices'))

# --- EVENTS MANAGEMENT ---
@admin_bp.route('/events')
@login_required
@admin_required
def events():
    events_list = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('admin/events.html', events=events_list)

@admin_bp.route('/events/add', methods=['POST'])
@login_required
@admin_required
def add_event():
    title = request.form.get('title')
    description = request.form.get('description')
    event_date_str = request.form.get('event_date')
    location = request.form.get('location', 'School Campus')
    category = request.form.get('category', 'Academic')

    if not title or not event_date_str:
        flash('Title and Event Date are required.', 'danger')
        return redirect(url_for('admin.events'))

    try:
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d')
    except ValueError:
        event_date = datetime.utcnow()

    event = Event(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        category=category
    )
    db.session.add(event)
    db.session.commit()
    flash('Event added successfully!', 'success')
    return redirect(url_for('admin.events'))

@admin_bp.route('/events/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'info')
    return redirect(url_for('admin.events'))

# --- GALLERY MANAGEMENT ---
@admin_bp.route('/gallery')
@login_required
@admin_required
def gallery():
    items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).all()
    return render_template('admin/gallery.html', items=items)

@admin_bp.route('/gallery/add', methods=['POST'])
@login_required
@admin_required
def add_gallery_item():
    title = request.form.get('title')
    category = request.form.get('category', 'Events')
    type = request.form.get('type', 'photo')
    media_url = request.form.get('media_url')
    description = request.form.get('description')

    if 'image_file' in request.files and request.files['image_file'].filename != '':
        file = request.files['image_file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        media_url = f"uploads/{filename}"

    if not title or not media_url:
        flash('Title and image/url are required.', 'danger')
        return redirect(url_for('admin.gallery'))

    item = GalleryItem(
        title=title,
        type=type,
        category=category,
        media_url=media_url,
        description=description
    )
    db.session.add(item)
    db.session.commit()
    flash('Gallery item added successfully!', 'success')
    return redirect(url_for('admin.gallery'))

@admin_bp.route('/gallery/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_gallery_item(id):
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Gallery item removed.', 'info')
    return redirect(url_for('admin.gallery'))

# --- DOWNLOADS MANAGEMENT ---
@admin_bp.route('/downloads')
@login_required
@admin_required
def downloads():
    resources = DownloadResource.query.order_by(DownloadResource.created_at.desc()).all()
    return render_template('admin/downloads.html', resources=resources)

@admin_bp.route('/downloads/add', methods=['POST'])
@login_required
@admin_required
def add_download():
    title = request.form.get('title')
    category = request.form.get('category', 'Syllabus')
    file_type = request.form.get('file_type', 'pdf')

    if 'resource_file' not in request.files:
        flash('File upload is required.', 'danger')
        return redirect(url_for('admin.downloads'))

    file = request.files['resource_file']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('admin.downloads'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Size calculation
    size_bytes = os.path.getsize(file_path)
    size_str = f"{round(size_bytes / (1024*1024), 2)} MB" if size_bytes > 1024*1024 else f"{round(size_bytes / 1024, 1)} KB"

    resource = DownloadResource(
        title=title,
        category=category,
        file_path=f"uploads/{filename}",
        file_size=size_str,
        file_type=file_type
    )
    db.session.add(resource)
    db.session.commit()
    flash('Download resource added!', 'success')
    return redirect(url_for('admin.downloads'))

@admin_bp.route('/downloads/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_download(id):
    resource = DownloadResource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    flash('Download resource deleted.', 'info')
    return redirect(url_for('admin.downloads'))

# --- ADMISSION INQUIRIES MANAGEMENT ---
@admin_bp.route('/inquiries')
@login_required
@admin_required
def inquiries():
    inquiries_list = AdmissionInquiry.query.order_by(AdmissionInquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries_list)

@admin_bp.route('/inquiries/update-status/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_inquiry_status(id):
    inquiry = AdmissionInquiry.query.get_or_404(id)
    status = request.form.get('status', 'Pending')
    inquiry.status = status
    db.session.commit()
    flash(f'Inquiry status updated to {status}.', 'success')
    return redirect(url_for('admin.inquiries'))

# --- SITE SETTINGS MANAGEMENT ---
@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    if request.method == 'POST':
        for key in ['school_name', 'school_address', 'school_phone', 'school_email', 'principal_name', 'principal_msg', 'principal_full_msg', 'chairperson_name', 'chairperson_msg', 'about_school']:
            if key in request.form:
                SiteSetting.set_val(key, request.form.get(key))
        flash('Site settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html')

# --- HERO BANNERS MANAGEMENT ---
@admin_bp.route('/banners')
@login_required
@admin_required
def banners():
    banner_list = HeroBanner.query.order_by(HeroBanner.order.asc()).all()
    return render_template('admin/banners.html', banners=banner_list)

@admin_bp.route('/banners/add', methods=['POST'])
@login_required
@admin_required
def add_banner():
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    button_text = request.form.get('button_text', 'Explore Academics')
    button_url = request.form.get('button_url', '/academics')
    order = int(request.form.get('order', 1))
    
    image_url = 'hero_1.jpg'
    if 'banner_file' in request.files and request.files['banner_file'].filename != '':
        file = request.files['banner_file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        image_url = f"uploads/{filename}"

    if not title:
        flash('Banner title is required.', 'danger')
        return redirect(url_for('admin.banners'))

    banner = HeroBanner(
        title=title,
        subtitle=subtitle,
        image_url=image_url,
        button_text=button_text,
        button_url=button_url,
        is_active=True,
        order=order
    )
    db.session.add(banner)
    db.session.commit()
    flash('Hero banner added successfully!', 'success')
    return redirect(url_for('admin.banners'))

@admin_bp.route('/banners/edit/<int:id>', methods=['POST'])
@login_required
@admin_required
def edit_banner(id):
    banner = HeroBanner.query.get_or_404(id)
    banner.title = request.form.get('title', banner.title)
    banner.subtitle = request.form.get('subtitle', banner.subtitle)
    banner.button_text = request.form.get('button_text', banner.button_text)
    banner.button_url = request.form.get('button_url', banner.button_url)
    banner.order = int(request.form.get('order', banner.order))
    
    if 'banner_file' in request.files and request.files['banner_file'].filename != '':
        file = request.files['banner_file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        banner.image_url = f"uploads/{filename}"

    db.session.commit()
    flash('Hero banner updated successfully!', 'success')
    return redirect(url_for('admin.banners'))

@admin_bp.route('/banners/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def toggle_banner(id):
    banner = HeroBanner.query.get_or_404(id)
    banner.is_active = not banner.is_active
    db.session.commit()
    status_str = 'activated' if banner.is_active else 'deactivated'
    flash(f'Hero banner {status_str}.', 'info')
    return redirect(url_for('admin.banners'))

@admin_bp.route('/banners/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_banner(id):
    banner = HeroBanner.query.get_or_404(id)
    db.session.delete(banner)
    db.session.commit()
    flash('Hero banner deleted.', 'info')
    return redirect(url_for('admin.banners'))

