from time import time



# Структурный паттерн Decorator.
# @AppRoute(routes=routes, url='/create-course/')
class AppRoute:
    """
    Так как методы декоратора вычисляются до запуска функций/классов, обернутых в этот декоратор,
    то на момент вызова мы получим словарь routes заполненный всеми необходимыми значениями."""

    def __init__(self, routes: dict, url: str):
        self.routes = routes
        self.url = url

    # Декоратор.
    def __call__(self, cls):
        self.routes[self.url] = cls()


# Структурный паттерн Decorator.
class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def time_decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time()
                func_result = func(*args, **kwargs)
                end_time = time()
                time_interval = end_time - start_time

                print(f"Debug --> {self.name} выполнялась {time_interval:2.3f} ms")

                return func_result

            return wrapper

        return time_decorator(cls)
