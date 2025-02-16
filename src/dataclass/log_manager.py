import logging
import io

class LogManager():
    def __init__(self, logger_name: str):
        self.set_baseConfig(logging.INFO)

        self.log = logging.getLogger(logger_name)
        self.handler = self._create_handler()
        self.log.addHandler(self.handler)

    def set_baseConfig(self, log_level) -> None:
        '''
        Set logging base config.

        :param log_level: Possible values = DEBUG, INFO, WARNING, ERROR, CRITICAL
        :return: None
        '''
        logging.basicConfig(
            level=log_level,
            format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
            datefmt="%y-%m-%d %H:%M",
        )

    def _create_handler(self):
        '''
        Create logging handler

        :return: handler
        '''
        self.string_io = io.StringIO()
        handler = logging.StreamHandler(self.string_io)
        return handler