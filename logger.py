import logging
import toml
import os


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

os.makedirs('logs', exist_ok=True)

# Configure logger
logging.basicConfig(
    level='DEBUG',
    handlers=[]
)

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('logs/app.log')
stream_handler.setFormatter(CustomFormatter())
file_handler.setFormatter(logging.Formatter(fmt = "%(asctime)s - %(name)s@%(filename)s:%(lineno)d - %(levelname)s - %(message)s"))
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


# Load the log level
config_file = 'config.toml'

# Set up global config
if os.path.isfile(config_file):
    config = toml.load(config_file)
else:
    logger.critical(f'Config file {config_file} not found.')

# Assign global config variables
level_logs = config['logs']['level']


logging.basicConfig(
    level=level_logs
)


if __name__ == '__main__':
    # TEst the logger
    print('Testing logger...')
    print()

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning')
    logger.error('This is an error')
    logger.critical('This is a critical error')