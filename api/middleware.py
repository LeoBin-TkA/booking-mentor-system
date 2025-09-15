from flask import request, jsonify, current_app
import jwt
from functools import wraps
from api.responses import error_response

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", None)
        if not auth:
            return error_response("Authorization header missing"), 401
        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return error_response("Invalid Authorization header"), 401
        token = parts[1]
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user_id = payload.get("sub")
        except jwt.ExpiredSignatureError:
            return error_response("Token expired"), 401
        except Exception:
            return error_response("Invalid token"), 401
        return f(*args, **kwargs)
    return wrapper

# Các hook đã có (log_request_info, error handler, options route) giữ lại
# Và trong create_app() bạn gọi middleware(app)
