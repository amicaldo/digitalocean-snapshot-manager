import os
import datetime


class Logger:
    __symbols: list = {
        'info': '[*]',
        'error': '[-]',
        'warning': '[~]'
    }

    __keys: list = {
        'info': 'INF',
        'error': 'ERR',
        'warning': 'WRN'
    }

    __color_format: list = {
        'info': '\033[94m%s\033[0m',
        'error': '\033[91m%s\033[0m',
        'warning': '\033[93m%s\033[0m',
        'time':  '\33[1m%s\033[0m'
    }

    __time_format: str = '%d/%m/%y %H:%M:%S'

    def __init__(self, log_path: str):
        self.__log_file: any = open(log_path, 'a')

    def __del__(self):
        self.__log_file.close()

    def __get_time(self) -> str:
        return str(datetime.datetime.now().strftime(self.__time_format))

    def __write(self, key: str, msg: str, time: str):
        self.__log_file.write(' '.join([
            self.__symbols[key],
            self.__keys[key],
            time,
            str(msg)
        ]) + '\n')

        self.__log_file.flush()

    def __output(self, key: str, msg: str, time: str):
        print(' '.join([
            self.__color_format[key],
            self.__color_format[key],
            self.__color_format['time'],
            str(msg)
        ]) % (
            self.__symbols[key],
            self.__keys[key],
            time
        ))

    def __log(self, key: str, msg: str, time: str):
        self.__write(key, msg, time)
        self.__output(key, msg, time)

    def info(self, msg: any):
        self.__log('info', str(msg), self.__get_time())

    def error(self, msg: any):
        self.__log('error', str(msg), self.__get_time())

    def warn(self, msg: any):
        self.__log('warning', str(msg), self.__get_time())
