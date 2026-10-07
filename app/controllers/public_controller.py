from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import (
    db, Notice, Event, GalleryItem, AcademicProgram, Facility,
    StaffMember, DownloadResource, AdmissionInquiry, ContactMessage,
    SiteSetting, HeroBanner, Testimonial
)

public_bp = Blueprint('public', __name__)

@public_bp.context_processor
def inject_global_settings():
    return {
        'school_name': SiteSetting.get_val('school_name', 'XYZ School and College'),
        'school_address': SiteSetting.get_val('school_address', 'Bafal, Kathmandu, Nepal'),
        'school_phone': SiteSetting.get_val('school_phone', '+977 98511-59700'),
        'school_email': SiteSetting.get_val('school_email', 'info@xyzschool.edu.np'),
        'urgent_notices': Notice.query.filter_by(is_urgent=True).order_by(Notice.published_date.desc()).all()
    }

@public_bp.route('/')
def home():
    banners = HeroBanner.query.filter_by(is_active=True).order_by(HeroBanner.order.asc()).all()
    notices = Notice.query.order_by(Notice.published_date.desc()).limit(5).all()
    events = Event.query.order_by(Event.event_date.asc()).limit(4).all()
    gallery = GalleryItem.query.order_by(GalleryItem.created_at.desc()).limit(6).all()
    facilities = Facility.query.limit(4).all()
    testimonials = Testimonial.query.order_by(Testimonial.order.asc()).all()
    
    principal_name = SiteSetting.get_val('principal_name', 'Ramesh S. Shrestha')
    principal_msg = SiteSetting.get_val('principal_msg', 'Delivering top-notch technical and qualitative education empowering students for future challenges...')
    principal_photo = SiteSetting.get_val('principal_photo', 'principal_portrait_1791286316731.jpg')
    
    return render_template(
        'public/index.html',
        banners=banners,
        notices=notices,
        events=events,
        gallery=gallery,
        facilities=facilities,
        testimonials=testimonials,
        principal_name=principal_name,
        principal_msg=principal_msg,
        principal_photo=principal_photo
    )

@public_bp.route('/about')
def about():
    programs = AcademicProgram.query.order_by(AcademicProgram.order.asc()).all()
    facilities = Facility.query.all()
    about_text = SiteSetting.get_val('about_school', 'XYZ School and College is a premier academic institution located in Bafal, Kathmandu...')
    return render_template('public/about.html', programs=programs, facilities=facilities, about_text=about_text)

@public_bp.route('/message-from-principal')
def message_principal():
    principal_name = SiteSetting.get_val('principal_name', 'Ramesh S. Shrestha')
    principal_msg = SiteSetting.get_val('principal_full_msg', 'Delivering top-notch technical and qualitative education...')
    principal_photo = SiteSetting.get_val('principal_photo', 'principal_portrait_1791286316731.jpg')
    return render_template('public/principal.html', name=principal_name, message=principal_msg, photo=principal_photo)

@public_bp.route('/message-from-chairperson')
def message_chairperson():
    chairperson_name = SiteSetting.get_val('chairperson_name', 'Mr. Indra Bahadur Maharjan')
    chairperson_msg = SiteSetting.get_val('chairperson_msg', 'Welcome to Kankali Secondary School. We aim to foster holistic growth...')
    chairperson_photo = SiteSetting.get_val('chairperson_photo', 'default_staff.png')
    return render_template('public/chairperson.html', name=chairperson_name, message=chairperson_msg, photo=chairperson_photo)

@public_bp.route('/our-team')
def team():
    teachers = StaffMember.query.filter_by(type='Teacher').order_by(StaffMember.order.asc()).all()
    smc = StaffMember.query.filter_by(type='SMC').order_by(StaffMember.order.asc()).all()
    pta = StaffMember.query.filter_by(type='PTA').order_by(StaffMember.order.asc()).all()
    return render_template('public/team.html', teachers=teachers, smc=smc, pta=pta)

@public_bp.route('/academics')
def academics():
    programs = AcademicProgram.query.order_by(AcademicProgram.order.asc()).all()
    facilities = Facility.query.all()
    return render_template('public/academics.html', programs=programs, facilities=facilities)

@public_bp.route('/facilities')
def facilities():
    facilities_list = Facility.query.all()
    return render_template('public/facilities.html', facilities=facilities_list)

@public_bp.route('/gallery')
def gallery():
    category_filter = request.args.get('category', 'all')
    if category_filter != 'all':
        items = GalleryItem.query.filter_by(category=category_filter).order_by(GalleryItem.created_at.desc()).all()
    else:
        items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).all()
    
    categories = db.session.query(GalleryItem.category).distinct().all()
    categories_list = [c[0] for c in categories]
    
    return render_template('public/gallery.html', items=items, categories=categories_list, active_category=category_filter)

@public_bp.route('/notices')
def notices():
    category = request.args.get('category', 'all')
    search_q = request.args.get('q', '')
    
    query = Notice.query
    if category != 'all':
        query = query.filter_by(category=category)
    if search_q:
        query = query.filter(Notice.title.ilike(f'%{search_q}%') | Notice.content.ilike(f'%{search_q}%'))
        
    notice_list = query.order_by(Notice.published_date.desc()).all()
    return render_template('public/notices.html', notices=notice_list, category=category, search_q=search_q)

@public_bp.route('/notice/<int:id>')
def notice_detail(id):
    notice = Notice.query.get_or_404(id)
    recent = Notice.query.filter(Notice.id != id).order_by(Notice.published_date.desc()).limit(5).all()
    return render_template('public/notice_detail.html', notice=notice, recent_notices=recent)

@public_bp.route('/events')
def events():
    events_list = Event.query.order_by(Event.event_date.asc()).all()
    return render_template('public/events.html', events=events_list)

@public_bp.route('/downloads')
def downloads():
    resources = DownloadResource.query.order_by(DownloadResource.created_at.desc()).all()
    return render_template('public/downloads.html', resources=resources)

@public_bp.route('/download-file/<int:id>')
def download_file(id):
    resource = DownloadResource.query.get_or_404(id)
    resource.download_count += 1
    db.session.commit()
    # Redirect to static file location
    return redirect(url_for('static', filename=resource.file_path))

@public_bp.route('/admission-inquiry', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        guardian_name = request.form.get('guardian_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        grade_applying = request.form.get('grade_applying')
        previous_school = request.form.get('previous_school')
        message = request.form.get('message')

        if not student_name or not guardian_name or not phone or not grade_applying:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('public.admission'))

        inquiry = AdmissionInquiry(
            student_name=student_name,
            guardian_name=guardian_name,
            phone=phone,
            email=email,
            grade_applying=grade_applying,
            previous_school=previous_school,
            message=message
        )
        db.session.add(inquiry)
        db.session.commit()
        flash('Thank you for submitting your admission inquiry! Our team will contact you shortly.', 'success')
        return redirect(url_for('public.admission'))

    return render_template('public/admission.html')

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('public.contact'))

        msg = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent successfully. We will get back to you soon!', 'success')
        return redirect(url_for('public.contact'))

    return render_template('public/contact.html')
