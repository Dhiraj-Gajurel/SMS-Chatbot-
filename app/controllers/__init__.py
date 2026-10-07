from app.controllers.public_controller import public_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.user_controller import user_bp
from app.controllers.chatbot_controller import chatbot_bp

__all__ = ['public_bp', 'auth_bp', 'admin_bp', 'user_bp', 'chatbot_bp']
