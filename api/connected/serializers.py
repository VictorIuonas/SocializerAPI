from marshmallow import Schema, fields, pre_dump


class DevConnectedResponseSchema(Schema):
    connected = fields.Boolean()
    organizations = fields.Method('get_organizations')

    @pre_dump(pass_many=False)
    def remove_unconnected_organizations(self, data, many):
        if not data['connected']:
            data.pop('organizations', None)

        return data

    def get_organizations(self, obj):
        if obj.get('organizations', None):
            return [org['name'] for org in obj['organizations']]
        return []


class ErrorResponseSchema(Schema):
    errors = fields.Method('get_error_messages')

    def get_error_messages(self, obj):
        return [str(error) for error in obj]
