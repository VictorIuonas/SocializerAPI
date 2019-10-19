from marshmallow import Schema, fields, pre_dump


class DevConnectedResponseSchema(Schema):
    connected = fields.Boolean()
    organizations = fields.List(fields.String)

    @pre_dump(pass_many=False)
    def remove_unconnected_organizations(self, data, many):
        if not data['connected']:
            data.pop('organizations', None)

        return data
