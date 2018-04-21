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
import socket
from sys import exit, stdout
from time import sleep


__version__ = '0.1'


class RSSrvCore:

    def __init__(self):
        """Initialize a shell server"""

        self.args = None
        self.arg_parser = ArgumentParser()


    def get_args(self):
        """Set argument options"""

        self.arg_parser.add_argument('--version', action = 'version',
                version = '%(prog)s ' + str(__version__))
        self.arg_parser.add_argument('port',
                action = 'store', type=int,
                help = ('set a file with which to do nothing'))

        self.args = self.arg_parser.parse_args()


    def main_event(self):
        """Connect to an incoming shell"""
        with socket.socket() as s:
            print('Binding to port ' + str(self.args.port))
            s.bind(('0.0.0.0', self.args.port))
            s.listen(1)
            conn, host = s.accept()
            print('Received connection from ' + str(host[0]) + \
                    ':' + str(host[1]) + '.')
            print('Type exit or enter EOF (ctrl-d) to exit')
            while True:
                try:
                    cmd = input('$ ')
                    conn.send(bytes(cmd, 'utf8'))
                    if cmd == 'exit':
                        conn.close()
                        s.close()
                        exit(0)
                    else:
                        recdata = conn.recv(16834)
                        if recdata:
                            stdout.buffer.write(recdata)
                        sleep(0.1)
                except EOFError:
                    conn.send(bytes('exit', 'utf8'))
                    conn.close()
                    s.close()
                    exit(0)


    def run_script(self):
        """Run the shell server program"""
        try:
            self.get_args()
            self.main_event()

        except KeyboardInterrupt:
            print('\nExiting on KeyboardInterrupt')


def main():
    thing = ListenCore()
    thing.run_script()


if __name__ == "__main__":
    main()
