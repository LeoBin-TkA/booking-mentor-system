from flask import Blueprint, request
from api.responses import success_response, not_found_response
from api.schemas.user import UserResponseSchema, UpdateUserSchema
from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository
from api.middleware import token_required

bp = Blueprint("user", __name__, url_prefix="/users")
user_service = UserService(UserRepository())
user_schema = UserResponseSchema()
update_schema = UpdateUserSchema()

@bp.route("/me", methods=["GET"])
@token_required
def me():
    user = user_service.get_by_id(request.user_id)
    if not user:
        return not_found_response("User not found")
    return success_response(user_schema.dump(user))
