#!/usr/bin/env python3

import logging, logging.handlers
from argparse import ArgumentParser

__version__ = '0.1'

def get_args():
    """Set argument options"""
    arg_parser = ArgumentParser()

    arg_parser.add_argument('--version', action = 'version',
            version = '%(prog)s ' + str(__version__))
    arg_parser.add_argument('-p',
            action = 'store', dest = 'port', type = int, default = 514,
            help = 'set the syslog server port (default 514)')
    arg_parser.add_argument('-f',
            action = 'store', dest = 'facility', default = 'local0',
            help = 'set the syslog facility (default local0)')
    arg_parser.add_argument('server',
            action = 'store',
            help = 'set the syslog server')
    arg_parser.add_argument('message',
            action = 'store',
            help = 'message to send via syslog')

    args = arg_parser.parse_args()

    return args

def sendlog(server, port, message, facility='local0'):
    """Send a log message"""
    # Set up syslog server:
    logger1 = logging.getLogger('syslogLogger')
    logger1.setLevel(logging.INFO)
    # Add handler to the logger
    handler1 = logging.handlers.SysLogHandler(
            address=(server, port),
            facility=facility)
    # Add formatter to the handler
    formatter1 = logging.Formatter('systemname: syslogtest: %(message)s')
    handler1.formatter = formatter1
    logger1.addHandler(handler1)
    logger1.info(msg)

def main():
    """Run the program"""
    args = get_args()
    sendlog(args.server, args.port, facility=args.facility)


if __name__ == "__main__":
    main()
