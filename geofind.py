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

import socket
import GeoIP
import sys
from argparse import ArgumentParser

__version__ = 0.1


def parse_args():
    """Get arguments"""
    
    parser = ArgumentParser()

    parser.add_argument('--version', action='version',
            version='%(prog)s ' + str(__version__))
    parser.add_argument('-f', '--full',
            action='store_true',
            help=('get full GeoIP output'))
    parser.add_argument('--data', action='store',
            default='/usr/share/GeoIP/GeoIPCity.dat',
            help=('set the .dat file to use'))
    parser.add_argument('hosts',
            metavar='HOST', nargs='*',
            help=('set a host to look up'))

    args = parser.parse_args()

    return args



def lookup_short(targets, data):
    """Get basic GeoIP data (city, region_name, country_name)"""

    geoquery = GeoIP.GeoIP(data, flags=0)

    for target in targets:
        
        addr = target
        attrs = {}
        print('\n==== GeoIP data for %s ====' %addr)
        
        try:
            ipaddr = socket.gethostbyname(addr)
            print('%s: %s' %('ip_addr', ipaddr))

            for x, y in geoquery.record_by_addr(ipaddr).items():
                attrs[x] = y

            print('%s, %s, %s' %(attrs['city'], attrs['region_name'],
                attrs['country_name']))

        except socket.gaierror:
            print('%s: Name or service not known' %addr)


def lookup(targets, data):
    """Get full GeoIP data"""

    geoquery = GeoIP.GeoIP(data, flags=0)

    for target in targets:
        
        addr = target
        attrs = {}
        print('\n==== GeoIP data for %s ====' %addr)
        
        try:
            ipaddr = socket.gethostbyname(addr)
            print('%15s: %s' %('ip_addr', ipaddr))

            for x, y in geoquery.record_by_addr(ipaddr).items():
                attrs[x] = y

            for x in sorted(attrs):
                print('%15s: %s' %(x, attrs[x]))

        except socket.gaierror:
            print('%s: Name or service not known' %addr)


def main():
    args = parse_args()
    
    if args.full:
        lookup(args.hosts, args.data)
    else:
        lookup_short(args.hosts, args.data)


if __name__ == "__main__":
    args = parse_args()
    
    if args.full:
        lookup(args.hosts, args.data)
    else:
        lookup_short(args.hosts, args.data)
