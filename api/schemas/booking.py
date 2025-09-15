from marshmallow import Schema, fields

class BookingRequestSchema(Schema):
    mentor_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    note = fields.Str()

class BookingResponseSchema(Schema):
    id = fields.Int(required=True)
    mentor_id = fields.Int()
    student_id = fields.Int()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    status = fields.Str()
