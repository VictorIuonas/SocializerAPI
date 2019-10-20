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
        return [org['name'] for org in obj['organizations']]
