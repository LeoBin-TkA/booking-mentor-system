from src.api.controllers.auth_controller import bp as auth_bp
from src.api.controllers.user_controller import bp as user_bp
from src.api.controllers.mentor_controller import bp as mentor_bp
from src.api.controllers.booking_controller import bp as booking_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(booking_bp)
    # nếu vẫn cần TODO
    app.register_blueprint(todo_bp)
