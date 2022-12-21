from datetime import datetime


# front controller
def secret_front(request):
    request['date'] = datetime.now().strftime("%Y-%b-%d %H:%M:%S")


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
