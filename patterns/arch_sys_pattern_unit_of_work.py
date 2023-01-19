from threading import local


# архитектурный системный паттерн - UnitOfWork
class UnitOfWork:
    """
    Паттерн UNIT OF WORK
    """
    # Создаю объект, способный скрывать значения от просмотра в отдельных потоках.
    # Работа с БД должна вестись в одном, отдельном потоке.
    current = local()
    # Списки в которых будут накапливаться все операции в рамках одной транзакции.
    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)
    # Запуск методов для работы со списками через маппер.
    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    def insert_new(self):
        print(self.new_objects)
        for obj in self.new_objects:
            print(f"Вывожу {self.MapperRegistry}")
            self.MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            self.MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    # Создать новый поток.
    # При начале работы с БД(Обращение к UnitWork) необходима инициализация нового потока.
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    # Сделать текущим потоком. set_current(None) - по сути - закрытие текущего потока.
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    # Получить текущий поток. Commit делается как раз через текущий поток.
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)
