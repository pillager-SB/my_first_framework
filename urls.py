from datetime import datetime
from views import Index, About, Contacts, PageNotExists


# front controller
def secret_front(request):
    request['date'] = datetime.now().strftime("%Y-%b-%d %H:%M:%S")


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/404/': PageNotExists(),
}
