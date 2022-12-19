from datetime import datetime
from views import Index, About, StudyPrograms, CoursesList, CreateCourse, CreateCategory, CategoryList, CopyCourse, \
    PageNotExists


# front controller
def secret_front(request):
    request['date'] = datetime.now().strftime("%Y-%b-%d %H:%M:%S")


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/study_programs/': StudyPrograms(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-course/': CopyCourse(),
    '/404/': PageNotExists(),
}
