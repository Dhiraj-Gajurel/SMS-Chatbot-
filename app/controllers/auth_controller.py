from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('public.home'))

    if request.method == 'POST':
        identity = request.form.get('identity', '').strip()
        password = request.form.get('password', '')

        if not identity or not password:
            flash('Please provide both username/email and password.', 'warning')
            return render_template('auth/login.html')

        user = User.query.filter(
            (User.username == identity) | 
            (User.email == identity)
        ).first()

        if user and user.check_password(password):
            if not user.is_admin():
                flash('Student login portal is disabled. Only administrator access is permitted.', 'danger')
                return render_template('auth/login.html')

            if not user.is_active:
                flash('Your account has been deactivated. Please contact administration.', 'danger')
                return render_template('auth/login.html')

            login_user(user, remember=True)
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
                
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('public.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    flash('Student registration is disabled.', 'info')
    return redirect(url_for('public.home'))
