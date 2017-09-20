#!/usr/bin/env python

#_MIT License
#_
#_Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
#_
#_Permission is hereby granted, free of charge, to any person obtaining a copy
#_of this software and associated documentation files (the "Software"), to deal
#_in the Software without restriction, including without limitation the rights
#_to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#_copies of the Software, and to permit persons to whom the Software is
#_furnished to do so, subject to the following conditions:
#_
#_The above copyright notice and this permission notice shall be included in all
#_copies or substantial portions of the Software.
#_
#_THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#_IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#_FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#_AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#_LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#_OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#_SOFTWARE.


import os
import threading
from argparse import ArgumentParser

__version__ = '0.1'

def parseargs():
    """set config options"""
    
    parser = ArgumentParser()

    parser.add_argument('--version', action='version',
            version='%(prog)s ' + str(__version__))
    parser.add_argument('-n', action='store',
            default='100', dest='tries',
            help=('set the number of passwords to check'))
    parser.add_argument('--file', action='store',
            default='rand-wordlist.txt',
            help=('set the wordlist file'))
    parser.add_argument('--hydra-args', action='store',
            default='', dest='hargs',
            help=('pass additional arguments to hydra'))
    parser.add_argument('--generate', action='store_true',
            help=('generate a random wordlist to use'))
    parser.add_argument('--user', action='store',
            default='root',
            help=('set the username to use (default: root)'))
    parser.add_argument('--service', action='store',
            default='ssh',
            help=('set the service to target (default: ssh)'))
    parser.add_argument('hosts', nargs='*',
            metavar='HOST',
            help=('set the target host'))

    args = parser.parse_args()

    return args


def wordlistgen(outfile):
    """Generate a 10 word random wordlist"""

    # Use completely random characters to minimize chance of a success
    os.popen('pwgen -sy1 10 10 > ' + outfile)


def wordlistsim(wordlist, host, user, service, runs,
        hargs):
    """Simulate a brute force attack by repeating a 10 word list"""

    for n in range(int(runs)):
        print('Starting run ' + str(n + 1) + '/' + str(runs) + \
                ' on host ' + host + '.')
        o = os.popen('hydra -t 4 -l ' + user + ' ' + hargs + ' -P ' + \
                wordlist + ' ' + host + ' ' + service).read()


def wordlistsimstart(wordlist, hosts, username, servicename, tries, hargs):
    """Start brute force attack simulations (one thread per host)"""
    
    #nruns = str(int(tries) // 10)
    
    # Set the number of runs
    with open(wordlist, 'r') as f:
        lines = f.readlines()
    
    nruns = int(tries) // len(lines)
    
    print('Target hosts: ' + str(hosts) + '\n' + \
            'User: ' + username + '\n' + \
            'Service: ' + servicename + '\n' + \
            'Max # of tries: ' + tries + '\n' + \
            'Additional hydra args: ' + hargs)

    # Start one thread per host and work in parallel
    for host in hosts:
        thread = threading.Thread(name=host,
                target=wordlistsim,
                args=(wordlist, host, username,
                    servicename, nruns,
                    hargs))
        #thread.daemon = True
        thread.start()


def runsim():
    """Run wordlist simulator program"""

    args = parseargs()

    if args.generate:
        wordlistgen(args.file)
    else:
        wordlistsimstart(args.file, args.hosts, args.user, args.service,
                args.tries, args.hargs)



def main():
    runsim()


if __name__ == "__main__":
    runsim()
