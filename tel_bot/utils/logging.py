import logging


class ZLogger():
    def __init__(self, filename) -> None:
        # Setup logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
            level=logging.INFO,
            filename=filename
        )
        self.logger = logging.getLogger("zerobits01-nano1 telegram bot")

    def log_text(self, msg, lvl):
        if hasattr(self.logger, lvl):
            method = getattr(self.logger, lvl)
            method(msg)

zlogger = ZLogger('zn-telebot.log')
