import logging
import sys
from datetime import datetime
from config.settings import get_settings

settings = get_settings()

class ColoredFormatter(logging.Formatter):
    """Custom formatter to make terminal debugging instant during the hackathon."""
    
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[1;91m'# Bold Red
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        time = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        # Format: [TIME] [LEVEL] - MESSAGE
        msg = f"{color}[{time}] [{record.levelname:^8}]{self.RESET} - {record.getMessage()}"
        return msg

def setup_logger():
    logger = logging.getLogger("OrionSync")
    
    # Avoid attaching multiple handlers if instantiated multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    
    logger.addHandler(console_handler)
    logger.propagate = False
    
    return logger

log = setup_logger()