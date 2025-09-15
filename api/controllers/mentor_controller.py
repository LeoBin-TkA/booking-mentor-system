from flask import Blueprint, request, jsonify
from services.mentor_service import MentorService
from infrastructure.repositories.mentor_repository import MentorRepository
from api.schemas.mentor import MentorRequestSchema, MentorResponseSchema
from datetime import datetime

bp = Blueprint("mentor", __name__, url_prefix="/mentors")

mentor_service = MentorService(MentorRepository())
request_schema = MentorRequestSchema()
response_schema = MentorResponseSchema()

# GET all mentors
@bp.route("/", methods=["GET"])
def list_mentors():
    mentors = mentor_service.list_mentors()
    return jsonify(response_schema.dump(mentors, many=True)), 200

# GET mentor by ID
@bp.route("/<int:mentor_id>", methods=["GET"])
def get_mentor(mentor_id):
    mentor = mentor_service.get_mentor(mentor_id)
    if not mentor:
        return jsonify({"message": "Mentor not found"}), 404
    return jsonify(response_schema.dump(mentor)), 200

# CREATE mentor
@bp.route("/", methods=["POST"])
def create_mentor():
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    now = datetime.utcnow()
    mentor = mentor_service.create_mentor(
        name=data["name"],
        expertise=data["expertise"],
        email=data["email"],
        created_at=now,
        updated_at=now
    )
    return jsonify(response_schema.dump(mentor)), 201

# UPDATE mentor
@bp.route("/<int:mentor_id>", methods=["PUT"])
def update_mentor(mentor_id):
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    mentor = mentor_service.update_mentor(
        mentor_id=mentor_id,
        name=data["name"],
        expertise=data["expertise"],
        email=data["email"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(mentor)), 200

# DELETE mentor
@bp.route("/<int:mentor_id>", methods=["DELETE"])
def delete_mentor(mentor_id):
    mentor_service.delete_mentor(mentor_id)
    return "", 204
