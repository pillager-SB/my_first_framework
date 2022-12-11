# get requests
class GetRequests:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            # разделяем параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        # Получаем параметры запроса.
        query_string = environ['QUERY_STRING']
        # Превращаем параметры в словарь.
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


# post requests
class PostRequests:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        """ Метод считывающий данные из среды WSGI."""
        # Получаем длину тела по ключу 'CONTENT_LENGTH', как str,
        # которую нужно вернуть в виде целого числа.
        # Если нет - определяем как 0.
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные, если они есть
        # env['wsgi.input'] -> <class '_io.BufferedReader'>
        # Если content_length не нулевой длины, то
        # запускаем режим чтения из файлоподобного объекта
        # и возвращаем его байтовое содержимое,
        # иначе - возврат пустой строки b''.
        data = env['wsgi.input'].read(content_length) if content_length else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        """Метод разбирающий данные и собирающий их в словарь"""
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        # получаем данные
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parse_wsgi_input_data(data)
        return data
