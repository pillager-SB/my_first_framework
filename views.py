from my_first_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None))


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', date=request.get('date', None))


class PageNotExists:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
