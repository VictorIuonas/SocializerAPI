from api import api
from api.connected.factories import build_create_connection_data_use_case
from api.connected.serializers import DevConnectedResponseSchema


@api.route('/connected/realtime/<dev1>/<dev2>', methods=['GET'])
def realtime(dev1, dev2):
    print(f'hello, world {dev1} and {dev2}')
    use_case = build_create_connection_data_use_case()

    result = use_case.execute(dev1, dev2)

    response_serializer = DevConnectedResponseSchema()

    response = response_serializer.dump(result.to_dict())

    return response
