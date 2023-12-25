from loguru import logger


my_logger = logger
my_logger.add('file_with_logs.log', format='{time} {level} {message}', level='INFO',
              rotation='30 MB')
