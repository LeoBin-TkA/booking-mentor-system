from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from api.schemas.user import RegisterSchema, LoginSchema, UserResponseSchema
from api.schemas.mentor import MentorRequestSchema, MentorResponseSchema
from api.schemas.booking import BookingRequestSchema, BookingResponseSchema

spec = APISpec(
    title="Mentor Booking API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("Register", schema=RegisterSchema)
spec.components.schema("Login", schema=LoginSchema)
spec.components.schema("UserResponse", schema=UserResponseSchema)
spec.components.schema("MentorRequest", schema=MentorRequestSchema)
spec.components.schema("MentorResponse", schema=MentorResponseSchema)
spec.components.schema("BookingRequest", schema=BookingRequestSchema)
spec.components.schema("BookingResponse", schema=BookingResponseSchema)
