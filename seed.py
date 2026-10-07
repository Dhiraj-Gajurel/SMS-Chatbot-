import os
from datetime import datetime, timedelta
from app import create_app
from app.models import (
    db, User, Notice, Event, GalleryItem, AcademicProgram,
    Facility, StaffMember, DownloadResource, AdmissionInquiry,
    ContactMessage, SiteSetting, HeroBanner, Testimonial
)

app = create_app()

with app.app_context():
    db.create_all()

    # 1. Create Default Users if not existing
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@xyzschool.edu.np',
            full_name='System Administrator',
            role='admin',
            phone='+977 98511-59700'
        )
        admin.set_password('admin123')
        db.session.add(admin)

    if not User.query.filter_by(username='student').first():
        student = User(
            username='student',
            email='student@xyzschool.edu.np',
            full_name='Aayush Maharjan',
            role='student',
            student_id='XYZ-2081-042',
            grade_class='Class 10-A',
            phone='+977 98412-34567'
        )
        student.set_password('student123')
        db.session.add(student)

    db.session.commit()

    # 2. Seed Site Settings
    settings_data = {
        'school_name': 'XYZ School and College',
        'school_address': 'Bafal, Kathmandu, Nepal',
        'school_phone': '+977 98511-59700',
        'school_email': 'info@xyzschool.edu.np',
        'principal_name': 'Ramesh S. Shrestha',
        'principal_msg': 'Delivering top-notch technical and qualitative education empowering students to excel in modern global opportunities while staying rooted in moral values.',
        'principal_full_msg': 'At XYZ School and College, Bafal, Kathmandu, we are committed to nurturing intellectual curiosity, character, and practical skills. Our state-of-the-art facilities, dedicated educators, and comprehensive curriculum prepare students to become leadership-oriented global citizens.',
        'chairperson_name': 'Mr. Indra Bahadur Maharjan',
        'chairperson_msg': 'XYZ School and College stands as a beacon of academic excellence and holistic development in Bafal, Kathmandu. We warmly invite students and parents to join our educational journey.',
        'about_school': 'XYZ School and College, located in the accessible and vibrant area of Bafal, Kathmandu, has been delivering quality education for decades. We offer comprehensive education from Pre-Primary up to Secondary (+2) & Higher Education Level with technical and general academic streams.'
    }

    for key, val in settings_data.items():
        setting = SiteSetting.query.filter_by(key=key).first()
        if not setting:
            db.session.add(SiteSetting(key=key, value=val))
        else:
            setting.value = val

    # 3. Seed Hero Banners
    if HeroBanner.query.count() < 4:
        HeroBanner.query.delete()
        banners = [
            HeroBanner(
                title='Welcome to XYZ School and College',
                subtitle='Bafal, Kathmandu — Shaping Future Leaders & Innovators',
                image_url='hero_1.jpg',
                button_text='Explore Academics',
                button_url='/academics',
                order=1,
                is_active=True
            ),
            HeroBanner(
                title='World-Class Science & Technology Labs',
                subtitle='Empowering Students with Modern Computer & Laboratory Infrastructure',
                image_url='hero_2.jpg',
                button_text='Campus Facilities',
                button_url='/facilities',
                order=2,
                is_active=True
            ),
            HeroBanner(
                title='Excellence in Sports & Athletics',
                subtitle='Nurturing Teamwork, Physical Fitness & Competitive Spirit',
                image_url='hero_3.jpg',
                button_text='School Calendar',
                button_url='/events',
                order=3,
                is_active=True
            ),
            HeroBanner(
                title='Admissions Open for Academic Session 2081',
                subtitle='Join Premier Pre-Primary, Secondary (+2) & Technical Education Streams',
                image_url='hero_4.jpg',
                button_text='Apply for Admission',
                button_url='/admission-inquiry',
                order=4,
                is_active=True
            )
        ]
        db.session.add_all(banners)
        db.session.commit()

    # 4. Seed Notices
    if not Notice.query.first():
        notices = [
            Notice(
                title='SEE Result 2081 Announcement & Outstanding Achievers Felicitation',
                slug='see-result-2081-announcement',
                category='Result',
                content='XYZ School and College proudly announces outstanding results in the SEE 2081 Examinations. We congratulate all students and teachers for securing 100% pass rate with high GPA distinction.',
                is_urgent=True,
                published_date=datetime.utcnow() - timedelta(days=1)
            ),
            Notice(
                title='Second Notice of Teacher Vacancy (Computer Science & Science)',
                slug='second-notice-teacher-vacancy',
                category='Vacancy',
                content='Applications are invited from eligible candidates for Secondary Level Computer Science Teacher and Basic Level Science Teacher posts. Qualified candidates must submit CV within 7 days.',
                is_urgent=True,
                published_date=datetime.utcnow() - timedelta(days=3)
            ),
            Notice(
                title='Quotation Notice for Computer Lab Hardware Upgrade',
                slug='quotation-notice-computer-lab-hardware',
                category='Quotation',
                content='Sealed quotations are invited from registered suppliers for supplying desktop computers, UPS units, and interactive smart whiteboards for school IT Lab.',
                is_urgent=False,
                published_date=datetime.utcnow() - timedelta(days=5)
            ),
            Notice(
                title='First Terminal Examination Routine Published for Classes 1 to 12',
                slug='first-terminal-exam-routine',
                category='Exam',
                content='The First Terminal Examinations for academic session 2081 will commence from next Sunday. Detailed routine is available in the downloads section.',
                is_urgent=False,
                published_date=datetime.utcnow() - timedelta(days=8)
            )
        ]
        db.session.add_all(notices)

    # 5. Seed Events
    if not Event.query.first():
        events = [
            Event(
                title='School & College Game Day & Inter-House Sports',
                description='Annual Inter-House Athletics, Football, Volleyball, and Chess tournaments at XYZ Sports Ground.',
                event_date=datetime.utcnow() + timedelta(days=5),
                location='XYZ Main Ground',
                category='Sports',
                is_featured=True
            ),
            Event(
                title='Parent-Teacher Interaction & Progress Report Distribution',
                description='Meeting of parents with grade teachers to evaluate terminal academic performance.',
                event_date=datetime.utcnow() + timedelta(days=12),
                location='Main Auditorium',
                category='Academic',
                is_featured=True
            ),
            Event(
                title='Science & Technology Exhibition 2081',
                description='Student projects demonstration featuring Robotics, Environmental Models, and IT solutions.',
                event_date=datetime.utcnow() + timedelta(days=20),
                location='Science Building',
                category='Cultural',
                is_featured=False
            )
        ]
        db.session.add_all(events)

    # 6. Seed Academic Programs & Facilities
    if not AcademicProgram.query.first():
        programs = [
            AcademicProgram(
                level='Pre-Primary Level',
                title='Montessori & Early Childhood Development',
                description='Child-centered learning environment with play-way methodology, sensory activities, and soft-skill foundation.',
                icon='fa-child',
                order=1
            ),
            AcademicProgram(
                level='Basic Level (Grades 1 - 8)',
                title='Comprehensive General Education',
                description='Strong foundation in Mathematics, Science, Nepali, English, Social Studies, and Practical Arts.',
                icon='fa-book-open',
                order=2
            ),
            AcademicProgram(
                level='Secondary & Higher Secondary (Grades 9 - 12)',
                title='Science, Management & Technical Streams (+2 & College)',
                description='Rigorous academic curriculum with specialization options in Science, Management, and Technical Education.',
                icon='fa-graduation-cap',
                order=3
            )
        ]
        db.session.add_all(programs)

    if not Facility.query.first():
        facilities = [
            Facility(
                title='Modern Computer Laboratory',
                description='High-speed internet, latest PC workstations, coding software, and dedicated IT instructors.',
                icon='fa-laptop-code'
            ),
            Facility(
                title='Well-Equipped Science Labs',
                description='Physics, Chemistry, and Biology laboratories equipped with modern instruments and safety apparatus.',
                icon='fa-flask'
            ),
            Facility(
                title='Resource-Rich Library',
                description='Thousands of reference books, journals, nepali/english literature, and e-learning digital catalog.',
                icon='fa-book-reader'
            ),
            Facility(
                title='Sports & Physical Training',
                description='Spacious playground for Football, Volleyball, Basketball, Athletics, and indoor games.',
                icon='fa-futbol'
            )
        ]
        db.session.add_all(facilities)

    # 7. Seed Staff Members
    if not StaffMember.query.first():
        staff = [
            StaffMember(
                name='Ramesh S. Shrestha',
                designation='Principal',
                type='Teacher',
                qualification='M.Ed, M.Sc Education',
                photo='principal_portrait_1791286316731.jpg',
                phone='+977 98511-59700',
                email='principal@xyzschool.edu.np',
                order=1
            ),
            StaffMember(
                name='Sunita Maharjan',
                designation='Vice Principal / Senior Academic Co-ordinator',
                type='Teacher',
                qualification='M.A. English',
                phone='+977 98419-87654',
                email='sunita@xyzschool.edu.np',
                order=2
            ),
            StaffMember(
                name='Mr. Indra Bahadur Maharjan',
                designation='SMC Chairperson',
                type='SMC',
                qualification='Community Leader & Educationist',
                order=1
            )
        ]
        db.session.add_all(staff)

    # 8. Seed Download Resources
    if not DownloadResource.query.first():
        downloads = [
            DownloadResource(
                title='College Prospectus & Admission Guidelines 2081',
                category='Form',
                file_path='uploads/sample_prospectus.pdf',
                file_size='2.4 MB',
                file_type='pdf'
            ),
            DownloadResource(
                title='First Terminal Examination Routine 2081',
                category='Routine',
                file_path='uploads/sample_routine.pdf',
                file_size='450 KB',
                file_type='pdf'
            ),
            DownloadResource(
                title='SEE Model Question Set (Mathematics & Science)',
                category='Model Question',
                file_path='uploads/sample_model_questions.pdf',
                file_size='1.8 MB',
                file_type='pdf'
            )
        ]
        db.session.add_all(downloads)

    # 9. Seed Gallery Items & Testimonials
    if not GalleryItem.query.first():
        gallery_items = [
            GalleryItem(
                title='XYZ School and College Main Building & Campus',
                type='photo',
                category='Campus',
                media_url='kankali_hero_banner_1791286291973.jpg',
                description='Beautiful view of our modern campus in Bafal, Kathmandu.'
            ),
            GalleryItem(
                title='Annual Sports Meet & Athletic Celebrations',
                type='photo',
                category='Sports',
                media_url='kankali_hero_banner_1791286291973.jpg',
                description='Students actively participating in track events.'
            )
        ]
        db.session.add_all(gallery_items)

    if not Testimonial.query.first():
        testimonials = [
            Testimonial(
                name='Prashant Karki',
                role='SEE Topper 2080 (GPA 3.95)',
                quote='XYZ School and College provided me with exceptional guidance, rigorous practice, and supportive teachers who believed in my potential.',
                grade_batch='SEE Batch 2080',
                order=1
            ),
            Testimonial(
                name='Saraswati Sharma',
                role='Parent',
                quote='The discipline, practical technical facilities, and caring environment at XYZ School and College have transformed my daughter into a confident learner.',
                grade_batch='Parent of Grade 9 Student',
                order=2
            )
        ]
        db.session.add_all(testimonials)

    db.session.commit()
    print("Database successfully seeded with XYZ School and College data!")
