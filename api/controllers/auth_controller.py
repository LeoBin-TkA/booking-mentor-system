from flask import Blueprint, request
from api.responses import success_response, error_response, validation_error_response
from api.requests import validate_request_schema
from api.schemas.user import RegisterSchema, LoginSchema, UserResponseSchema
from services.auth_service import AuthService
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.services.email_service import send_email

bp = Blueprint("auth", __name__, url_prefix="/auth")
   pip install -r requirements.txt
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_response = UserResponseSchema()

user_repo = UserRepository()            # hoặc inject từ dependency_container
auth_service = AuthService(user_repo)

@bp.route("/register", methods=["POST"])
def register():
    data_or_resp = validate_request_schema(register_schema)
    if hasattr(data_or_resp, "status_code"):
        return data_or_resp  # validation error response
    data = data_or_resp

    try:
        user = auth_service.register(data["email"], data["password"], data.get("name"))
        # gửi email chào mừng (non-blocking recommended via background job)
        send_email(user.email, "Welcome", "Thanks for registering!")
        return success_response(user_response.dump(user), message="Registered"), 201
    except Exception as e:
        return error_response(str(e), 400)

@bp.route("/login", methods=["POST"])
def login():
    data_or_resp = validate_request_schema(login_schema)
    if hasattr(data_or_resp, "status_code"):
        return data_or_resp
    data = data_or_resp
    try:
        token = auth_service.login(data["email"], data["password"])
        return success_response({"token": token})
    except Exception as e:
        return error_response(str(e), 401)
