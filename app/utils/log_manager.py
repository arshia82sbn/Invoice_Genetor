import logging
from threading import Lock

class LogManager:
    _instance = None
    _lock = Lock()
    _initilized = False
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        if not LogManager._initilized:
            return
        with LogManager._lock:
            if not LogManager._initilized:
                return

            # Create logger
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

            # Set format for logger
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # Create a console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.DEBUG)

            # check for handling
            if not self.logger.handlers:
                self.logger.addHandler(console_handler)

            LogManager._initilized = True
    def get_logger(self):
        return self.logger

# Set for the global access
def get_logger(self):
        return LogManager().get_logger()
