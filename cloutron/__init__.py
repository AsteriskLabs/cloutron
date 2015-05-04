import os
import logging
import logging.config

import cloutron
from .main import main

import plugin

from scruffy import Environment

# scruffy environment containing config, plugins, etc
env = None
config = None

# reference to debugger adaptor
debugger = None

# plugin commands
commands = None

loaded = False

def setup_env():
    global env, config
    env = Environment({
        'dir':  {
            'path': '~/.cloutron',
            'create': True,
            'mode': 448 # 0700
        },
        'files': {
            'config': {
                'type':     'config',
                'default':  {
                    'path':     'config/default.cfg',
                    'rel_to':   'pkg',
                    'pkg':      'cloutron'
                },
                'read':     True
            },
            'local_plugins': {
                'type':     'plugin_dir',
                'name':     'plugins',
                'create':   True
            },
            'internal_plugins': {
                'type':     'plugin_dir',
                'name':     'plugins',
                'rel_to':   'pkg',
                'pkg':      'cloutron'
            }
        },
        'basename': 'cloutron'
    })
    config = env['config']

    # create shared instance of plugin manager
    plugin.pm = plugin.PluginManager()

LOGGER_DEFAULT = {
    'handlers': ['null'],
    'level': 'DEBUG',
    'propagate': False
}

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {'format': 'cloutron: [%(levelname)s] %(message)s'}
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'null': {
            'class': 'logging.NullHandler'
        }
    },
    'loggers': {
        '':         LOGGER_DEFAULT,
        'debugger': LOGGER_DEFAULT,
        'core':     LOGGER_DEFAULT,
        'main':     LOGGER_DEFAULT,
        'api':      LOGGER_DEFAULT,
        'view':     LOGGER_DEFAULT,
        'plugin':   LOGGER_DEFAULT,
    }
}

def setup_logging(logname=None):
    # configure logging
    logging.config.dictConfig(LOG_CONFIG)

    # enable the debug_file in all the loggers if the config says to
    if config and 'general' in config and config['general']['debug_logging']:
        if logname:
            filename = 'cloutron_{}.log'.format(logname)
        else:
            filename = 'cloutron.log'
        for name in LOG_CONFIG['loggers']:
            h = logging.FileHandler(cloutron.env.path_to(filename), delay=True)
            h.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)-7s %(filename)12s:%(lineno)-4s %(funcName)20s -- %(message)s"))
            logging.getLogger(name).addHandler(h)

    logging.info("======= cloutron - DEFENDER OF THE poopiNIVERSE [debug log] =======")

    return logging.getLogger(logname)

# Python 3 shim
if not hasattr(__builtins__, "xrange"):
    xrange = range

# Setup the Voltron environment
setup_env()