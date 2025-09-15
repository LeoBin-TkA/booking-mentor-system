from flask import Blueprint, request, jsonify
from services.booking_service import BookingService
from infrastructure.repositories.booking_repository import BookingRepository
from api.schemas.booking import BookingRequestSchema, BookingResponseSchema
from datetime import datetime

bp = Blueprint("booking", __name__, url_prefix="/bookings")

booking_service = BookingService(BookingRepository())
request_schema = BookingRequestSchema()
response_schema = BookingResponseSchema()

# GET all bookings
@bp.route("/", methods=["GET"])
def list_bookings():
    bookings = booking_service.list_bookings()
    return jsonify(response_schema.dump(bookings, many=True)), 200

# GET booking by ID
@bp.route("/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = booking_service.get_booking(booking_id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    return jsonify(response_schema.dump(booking)), 200

# CREATE booking
@bp.route("/", methods=["POST"])
def create_booking():
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    now = datetime.utcnow()
    booking = booking_service.create_booking(
        mentor_id=data["mentor_id"],
        user_id=data["user_id"],
        schedule_time=data["schedule_time"],
        status=data["status"],
        created_at=now,
        updated_at=now
    )
    return jsonify(response_schema.dump(booking)), 201

# UPDATE booking
@bp.route("/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    booking = booking_service.update_booking(
        booking_id=booking_id,
        mentor_id=data["mentor_id"],
        user_id=data["user_id"],
        schedule_time=data["schedule_time"],
        status=data["status"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(booking)), 200

# DELETE booking
@bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    booking_service.delete_booking(booking_id)
    return "", 204
