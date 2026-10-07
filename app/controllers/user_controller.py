from flask import Blueprint, redirect, url_for, flash

user_bp = Blueprint('user', __name__, url_prefix='/portal')

@user_bp.route('/dashboard')
@user_bp.route('/profile')
def dashboard():
    flash('Student portal is disabled.', 'info')
    return redirect(url_for('public.home'))
