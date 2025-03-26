import logging
import sys

class Logger:
    def __init__(self, name: str = ''):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        stdout = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S'
        )
        stdout.setFormatter(formatter)
        self.logger.addHandler(stdout)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)