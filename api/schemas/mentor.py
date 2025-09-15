from marshmallow import Schema, fields

class MentorRequestSchema(Schema):
    name = fields.Str(required=True)
    expertise = fields.List(fields.Str(), required=True)
    bio = fields.Str()

class MentorResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str()
    expertise = fields.List(fields.Str())
    bio = fields.Str()
