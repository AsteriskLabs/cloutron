import os
import argparse
import logging
import traceback
import logging
import logging.config

import cloutron
from .view import *
from .plugin import *

log = logging.getLogger('main')

def main(debugger=None):
    cloutron.setup_logging('main')

    # Set up command line arg parser
    parser = argparse.ArgumentParser()
    parser.register('action', 'parsers', AliasedSubParsersAction)
    parser.add_argument('--debug', '-d', action='store_true', help='print debug logging')
    top_level_sp = parser.add_subparsers(title='subcommands', description='valid subcommands')
    view_parser = top_level_sp.add_parser('view', help='display a view', aliases=('v'))
    view_parser.register('action', 'parsers', AliasedSubParsersAction)
    view_sp = view_parser.add_subparsers(title='views', description='valid view types', help='additional help')

    # Set up a subcommand for each view class
    pm = PluginManager()
    for plugin in pm.view_plugins:
        pm.view_plugins[plugin].view_class.configure_subparser(view_sp)

    # Parse args
    args = parser.parse_args()
    if args.debug:
        cloutron.config['general']['debug_logging'] = True
        cloutron.setup_logging('main')

    # Instantiate and run the appropriate module
    inst = args.func(args, loaded_config=cloutron.config)
    inst.pm = pm
    try:
        inst.run()
    except Exception as e:
        log.error("Exception running module {}: {}".format(inst.__class__.__name__, traceback.format_exc()))
        print("Encountered an exception while running the view '{}':\n{}".format(inst.__class__.__name__, traceback.format_exc()))
    except KeyboardInterrupt:
        suppress_exit_log = True
    inst.cleanup()

if __name__ == "__main__":
    main()
