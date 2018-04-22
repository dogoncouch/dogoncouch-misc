#!/usr/bin/env python3

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
import re
from datetime import datetime
from time import sleep


__version__ = '0.1'


class LogFloodCore:

    def __init__(self):
        """Initialize a log flood core object"""

        self.args = None
        self.arg_parser = ArgumentParser()
        self.config = None


    def get_args(self):
        """Set argument options"""

        self.arg_parser.add_argument('--version', action = 'version',
                version = '%(prog)s ' + str(__version__))
        self.arg_parser.add_argument('-m',
                action = 'store', type=int,
                dest = 'maxevents', metavar = 'N', default = 100,
                help = ('exit after N events'))
        self.arg_parser.add_argument('-p',
                action = 'store', type=int,
                dest = 'sleepcount', metavar = 'N', default = 100,
                help = ('pause every N events (default 100)'))
        self.arg_parser.add_argument('-t',
                action = 'store', type = float,
                dest = 'sleeptime', metavar = 'S.F', default = 0.1,
                help = ('set length of pause in seconds (default 0.1)'))
        self.arg_parser.add_argument('files',
                action = 'store', metavar='FILE', nargs = '+',
                help = ('set a log file to flood'))

        self.args = self.arg_parser.parse_args()


    def main_event(self):
        """Flood new events to log files"""
        # Collect events
        rawevents = {}
        linenumbers = {}
        for logfile in self.args.files:
            with open(logfile, 'r') as f:
                rawevents[logfile] = f.readlines()[-1000:]
                linenumbers[logfile] = 0

        # Strip date stamps
        rex = re.compile(
                r'^[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}(.*$)')
        events = {}
        for logfile in self.args.files:
            events[logfile] = []
            for rawevent in rawevents[logfile]:
                match = rex.findall(rawevent)
                if match:
                    events[logfile].append(match[0])

        # Delete raw events to free memory
        del(rawevents)

        # Flood events with new date stamps
        self.eventcount = 0
        sleepcount = 0
        self.starttime = datetime.now()
            print('Starting logflood at ' + \
                    self.starttime..strftime('%b %d %H:%M:%S') + '.')
        while True:
            tstamp = datetime.now().strftime('%b %d %H:%M:%S')
            for logfile in self.args.files:
                if sleepcount == self.args.sleepcount:
                    sleep(self.args.sleeptime)
                    sleepcount = 0
                if self.args.maxevents:
                    if self.eventcount == self.args.maxevents:
                        self.final_output()
                        exit(0)
                try:
                    event = tstamp + \
                            events[logfile][linenumbers[logfile]]
                    linenumbers[logfile] += 1
                except IndexError:
                    event = tstamp + events[logfile][0]
                    linenumbers[logfile] = 1
                with open(logfile, 'a') as f:
                    f.write(event + '\n')
                    sleepcount +=1
                    self.eventcount += 1


    def final_output(self):
        """Print a summary"""
        runtime = datetime.now() - self.starttime
        print('Wrote ' + str(self.eventcount) + ' events in ' + \
                str(runtime.days) + 'days, '+ \
                str(int(runtime.total_seconds() // 60 // 60)) + \
                'hours, ' + \
                str(int(runtime.total_seconds() // 60 % 60)) + \
                'minutes, ' + \
                str(int(runtime.total_seconds() % 60 % 60)) + \
                'seconds.\nAverage ' + str(int(
                    self.eventcount / runtime.total_seconds())) + \
                            ' events per second.')


    def run_script(self):
        """Run the log flood program"""
        try:
            self.get_args()
            self.main_event()

        except KeyboardInterrupt:
            self.final_output()
            print('\nExiting on KeyboardInterrupt')


def main():
    thing = LogFloodCore()
    thing.run_script()


if __name__ == "__main__":
    main()
