#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2018 Dan Persons (dpersonsdev@gmail.com)
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
        self.arg_parser.add_argument('-f',
                action = 'store_true', dest = 'force',
                help = ('bind to sockets that are already in use'))
        self.arg_parser.add_argument('port',
                action = 'store', type=int,
                help = ('set the local port'))

        self.args = self.arg_parser.parse_args()


    def main_event(self):
        """Connect to an incoming shell"""
        with socket.socket() as s:
            if self.args.force:
                print('Enabling socket address reuse')
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print('Binding to port ' + str(self.args.port))
            s.bind(('0.0.0.0', self.args.port))
            s.listen(1)
            conn, host = s.accept()
            print('Received connection from ' + str(host[0]) + \
                    ':' + str(host[1]) + '.')
            remotehost, remotepyversion = str(
                    conn.recv(1024))[2:-1].split(':')
            print('Remote hostname: ' + remotehost + '.\n' + \
                    'Remote Python major version: ' + remotepyversion + '.')
            remotepyversion = int(remotepyversion)
            #print('Remote Python major version: ' + remotepyversion + '.')
            print('Type exit or enter EOF (ctrl-d) to exit.')
            while True:
                try:
                    cmd = input(remotehost + '$ ')
                    if cmd == 'exit':
                        conn.send(bytes(cmd, 'utf8'))
                        conn.close()
                        s.close()
                        exit(0)
                    else:
                        conn.send(bytes(cmd, 'utf8'))
                        recdata = conn.recv(16834)
                        if remotepyversion == 2:
                            if recdata and recdata != ':':
                                stdout.buffer.write(recdata)
                        else:
                            if recdata and recdata != bytes('\n', 'utf8'):
                                stdout.buffer.write(recdata)
                except EOFError:
                    conn.send(bytes('exit', 'utf8'))
                    print('exit')
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
    thing = RSSrvCore()
    thing.run_script()


if __name__ == "__main__":
    main()
