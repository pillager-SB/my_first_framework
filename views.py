from datetime import date
from my_first_framework.templator import render
from patterns.creating_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main')
routes = {}


# Контроллер(Главная).
@AppRoute(routes=routes, url='/')
class Index:
    @Debug('Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# Контроллер(О нас).
@AppRoute(routes=routes, url='/about/')
class About:
    @Debug('About')
    def __call__(self, request):
        return '200 OK', render('about.html')


# Контроллер(Расписания).
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @Debug('StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study_programs.html', date=date.today())


# Контроллер(404 Страница не найдена).
@AppRoute(routes=routes, url='/404/')
class PageNotExists:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Контроллер(Список курсов).
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug('CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render(
                'course_list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'Курсы еще не были добавлены.'


# Контроллер(Создать курс).
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug('CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':  # Если метод POST
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render(
                'course_list.html', objects_list=category.courses, name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'Категории еще не были добавлены.'


# Контроллер(Создать категорию).
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug('CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':  # Если метод POST
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None

            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


# Контроллер(Список категорий).
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug('CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


# Контроллер(Копировать курс).
@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug('CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=site.courses, name=new_course.category.name)
        except KeyError:
            return '200 OK', 'Курс не был добавлен.'
