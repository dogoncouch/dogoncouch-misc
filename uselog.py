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


import psutil
from time import sleep
import syslog
from argparse import ArgumentParser

__version__ = 0.1

facilities = {
        'local0': syslog.LOG_LOCAL0,
        'local1': syslog.LOG_LOCAL1,
        'local2': syslog.LOG_LOCAL2,
        'local3': syslog.LOG_LOCAL3,
        'local4': syslog.LOG_LOCAL4,
        'local5': syslog.LOG_LOCAL5,
        'local6': syslog.LOG_LOCAL6,
        'local7': syslog.LOG_LOCAL7
        }


class SystemUsageLogger:

    def __init__(self, facilityname):

        syslog.openlog(facility=facilities[facilityname])


    def do_watch(self, interval, tempfile, notemp = False):

        while True:
            cpu = str(psutil.cpu_percent())
            mem = str(psutil.virtual_memory()[2])

            msg = 'System usage: CPU: ' + cpu + '% Mem: ' + mem + '%'
                    
            if not notemp:
                with open(tempfile,
                        'r') as f:
                    cputmpraw = float(f.read()) / 1000
                cputmp = "%.1f'C" % cputmpraw

                msg += ' CPUTemp: ' + cputmp
        
            syslog.syslog(syslog.LOG_INFO, msg)
        
            sleep(interval * 60)


def parse_args():
    """Get arguments"""

    parser = ArgumentParser()

    parser.add_argument('--version', action='version',
            version='%(prog)s ' + str(__version__))
    parser.add_argument('--interval',
            action='store', type=int, default=2,
            help=('set logging interval in minutes (default 2)'))
    parser.add_argument('--facility',
            action='store', default='local1',
            help=('set logging facility (local0-7, default local1)'))
    parser.add_argument('--notemp',
            action='store_true',
            help=('do not log CPU temperature'))
    parser.add_argument('--tempfile',
            action='store',
            default='/sys/class/thermal/thermal_zone0/temp',
            help=('set a file for temperature readings'))

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    syswatch = SystemUsageLogger(args.facility)
    syswatch.do_watch(args.interval, args.tempfile, notemp=args.notemp)

if __name__ == "__main__":
    args = parse_args()
    syswatch = SystemUsageLogger(args.facility)
    syswatch.do_watch(args.interval, args.tempfile, notemp=args.notemp)

