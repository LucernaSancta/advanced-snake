import toml
import os
import logging
from logging.handlers import RotatingFileHandler


# Customized code form https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class CustomFormatter(logging.Formatter):

    grey = '\x1b[38;21m'
    green = '\x1b[0;32m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[33;20m'
    red = '\x1b[31;20m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    format = '%(levelname)s - %(message)s'

    FORMATS = {
        logging.DEBUG:    f'{blue    }[%(levelname)s] %(message)s{reset}',
        logging.INFO:     f'{green   }[%(levelname)s]{reset} %(message)s{reset}',
        logging.WARNING:  f'{yellow  }[%(levelname)s] %(message)s{reset}',
        logging.ERROR:    f'{red     }[%(levelname)s] %(message)s{reset}',
        logging.CRITICAL: f'{bold_red}[%(levelname)s] %(message)s{reset}'
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Load the log level
config_file = 'config.json'

# Set up global config
if os.path.isfile(config_file):
    config = toml.load(config_file)
else:
    logging.critical(f'Config file {config_file} not found.')

# Assign global config variables
cmd_level = config['logger']['console_level']
file_level = config['logger']['file_level']
max_file_size=config['logger']['max_file_size']
max_file_count=config['logger']['max_file_count']


# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logger
logging.basicConfig(
    level='DEBUG',
    handlers=[]
)

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = RotatingFileHandler('logs/app.log', maxBytes=max_file_size, backupCount=max_file_count)
stream_handler.setFormatter(CustomFormatter())
file_handler.setFormatter(logging.Formatter(fmt = "%(asctime)s - %(name)s@%(filename)s:%(lineno)d - %(levelname)s - %(message)s"))
stream_handler.setLevel(cmd_level)
file_handler.setLevel(file_level)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)



if __name__ == '__main__':
    # Test the logger
    print('Testing logger...')
    print()

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning')
    logger.error('This is an error')
    logger.critical('This is a critical error')