from copy import deepcopy
from quopri import decodestring
from .behavioral_patterns import FileWriter, Subject

# Относится к паттерну "Фабричный метод":
# Абстрактный класс:

class User:  # Абстрактный пользователь.
    def __init__(self, name):
        self.name = name


# Подклассы-потомки:
class Teacher(User):
    ...


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# Порождающая фабрика.
class UserFactory:
    # Словарь-связь типа и класса порождаемого объекта.
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# Относится к паттерну "Prototype":
# Абстрактный класс:
class CoursePrototype:
    # Нужно для реализации возможности создания новых объектов курсов методом копирования.
    def clone(self):  # Создание курсов копированием.
        return deepcopy(self)


# Комбинация паттернов "Фабричный метод" и Прототип:
class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# Подклассы-потомки:
class InteractiveCourse(Course):
    ...


class RecordCourse(Course):
    ...


# Порождающая фабрика.
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# категория
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    # Использование фабричного метода.
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    # Использование фабричного метода.
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, category_id):
        for item in self.categories:
            print('item', item.id)
            if item.id == category_id:
                return item
        raise Exception(f'Нет категории с id = {category_id}')

    @staticmethod
    # Использование фабричного метода.
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Singleton.
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)