from api import api


# @api.route('/connected/realtime/{dev1}/{dev2}')
@api.route('/connected/realtime')
def realtime():
    return 'hello, world'
