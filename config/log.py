import logging

logger = logging.getLogger('__main__')
logger.setLevel(logging.INFO)
formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('config/myapp.log')
file_handler.setFormatter(formater)
logger.addHandler(file_handler)