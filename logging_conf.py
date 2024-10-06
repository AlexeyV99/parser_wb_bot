import sys
import os
import datetime


base_dir = os.getcwd()
uniq_file_name = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')


dict_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        "fileFormatter": {
            'format':   "%(asctime)s | "
                        "%(levelname)-8s | "
                        # "%(name)s | "
                        "%(message)-30s | "
                        "%(filename)s:%(lineno)s",
            'date-fmt': '%Y-%m-%dT%H:%M:%S%Z'
        },
        "consoleFormatter": {
            'format':   #"%(asctime)s | "
                        "%(levelname)-8s | "
                        # "%(name)s | "
                        "%(message)-30s | "
                        "%(filename)s:%(lineno)s",
            'date-fmt': '%Y-%m-%dT%H:%M:%S%Z'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': "consoleFormatter",
            'stream': sys.stdout
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'fileFormatter',
            'filename': f'{base_dir}/logs/logfile.log',
            # 'mode': 'w'
        },
        'rotatingFileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'fileFormatter',
            'filename': f'{base_dir}/logs/logfile.log',
            # 'mode': 'w',
            'maxBytes': 1024*1024*10,
            'backupCount': 20
        },
        'timedRotatingFileHandler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'fileFormatter',
            'filename': f'{base_dir}/logs/logfile.log',
            # 'mode': 'w',
            'when': 'h',
            'interval': 1,
            'backupCount': 20
        }
    },
    'loggers': {
        'appLogger': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler',
                         # 'timedRotatingFileHandler',
                         'rotatingFileHandler',
                         # 'fileHandler'
                         ],
            'propagate': False,
        },
    },
    'root': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler'],
    }
}
