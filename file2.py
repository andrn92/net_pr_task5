import os
import datetime
import json


def logger(path):
    def __logger(old_function):
        data_dict = {}
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            date_call = datetime.datetime.now()
            data_dict['name'] = '{}'.format(old_function.__name__)
            data_dict['date_time'] = str(date_call)
            data_dict['args'] = [*args]
            data_dict['kwargs'] = {**kwargs}
            data_dict['result'] = result
            with open(path, 'w') as f:
                json.dump(data_dict, f, ensure_ascii=False)
            return result

        return new_function

    return __logger


def run():
    file_path = '/home/andrey/net_task4_pr/main2.log'
    some_logger = logger(path=file_path)
    # @some_logger
    def add_func(a, b):
        return a + b

    add_func = some_logger(add_func)
    print(add_func(5, 7))


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
     test_2()
    #  run()
