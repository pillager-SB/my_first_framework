from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    # templates - указываем место, где искать шаблоны.
    # Создаем окружение.
    env = Environment()
    # Загружаем в него содержимое из templates, включая вложения.
    env.loader = FileSystemLoader(folder)
    # Получаем возможность обратиться к шаблону по имени.
    template = env.get_template(template_name)
    # Возвращаем рендер выбранного шаблона.
    return template.render(**kwargs)
