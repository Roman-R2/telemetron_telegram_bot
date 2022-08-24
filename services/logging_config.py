"""Кофнфиг серверного логгера"""
from logger import GetLogger

LOGGER = GetLogger(logger_name='server_logger').get_logger()

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
