#!/usr/bin/env python

# MIT License
# 
# Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from argparse import ArgumentParser
from argparse import FileType
from configparser import ConfigParser
from os.path import isfile


__version__ = '0.1'


def get_args():
    """Set argument options"""

    arg_parser = ArgumentParser()

    arg_parser.add_argument('--version', action = 'version',
            version = '%(prog)s ' + str(__version__))
    arg_parser.add_argument('-c',
            action = 'store', dest = 'config',
            default = '/etc/nothing.conf',
            help = ('set the config file'))
    arg_parser.add_argument('--full',
            action = 'store_true',
            help = ('Do nothing to the fullest'))
    arg_parser.add_argument('files',
            type = FileType('r'), metavar='FILE', nargs = '?',
            help = ('set a file with which to do nothing'))

    args = arg_parser.parse_args()

    return args


def get_config(configfile):
    """Read the config file"""

    config = ConfigParser()
    
    if isfile(configfile):
        myconf = args.config
        config.read(myconf)

    else: return None


def main_event():
    """Do the actual nothing"""
    pass


def run_script():
    """Run the program that does nothing"""
    try:
        args = get_args()
        config = get_config(args.config)
        main_event()

    except KeyboardInterrupt:
        print('\nExiting on KeyboardInterrupt')


def main():
    run_script()


if __name__ == "__main__":
    main()
