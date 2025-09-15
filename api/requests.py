from flask import request, jsonify

def get_request_data():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    return data

def validate_request_schema(schema):
    """
    Returns data dict if ok, otherwise returns a flask Response (error).
    Controller should check isinstance(result, Response) or check .status_code attribute.
    """
    data_or_resp = get_request_data()
    # nếu get_request_data trả Response thì trả ngay
    if hasattr(data_or_resp, "status_code"):
        return data_or_resp
    data = data_or_resp
    errors = schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 422
    return data

# bỏ các handle_*_request() rỗng hoặc implement nếu bạn muốn chung handling
