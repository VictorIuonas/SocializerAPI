from flask import jsonify

from api import api
from api.connected.serializers import DevConnectedResponseSchema, ErrorResponseSchema


@api.route('/connected/realtime/<dev1>/<dev2>', methods=['GET'])
def realtime(dev1, dev2):
    from connected.factories import build_create_connection_data_use_case
    use_case = build_create_connection_data_use_case()

    result, errors = use_case.execute(dev1, dev2)

    if errors:
        errors_serializer = ErrorResponseSchema()
        response = errors_serializer.dump(errors)
    else:
        response_serializer = DevConnectedResponseSchema(only=['connected', 'organizations'])
        response = response_serializer.dump(result)

    return response


@api.route('/connected/registered/<dev1>/<dev2>', methods=['GET'])
def registered(dev1, dev2):
    from connected.factories import build_get_connection_history_use_case
    use_case = build_get_connection_history_use_case()

    result, errors = use_case.execute(dev1, dev2)

    if not errors:
        response_serializer = DevConnectedResponseSchema()
        response = response_serializer.dump(result, many=True)
        response = jsonify(response)
    else:
        errors_serializer = ErrorResponseSchema()
        response = errors_serializer.dump(errors)

    return response
