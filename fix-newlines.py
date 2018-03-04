#!/usr/bin/env python

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


__version__ = '0.1'


def get_args():
    """Set argument options"""

    arg_parser = ArgumentParser()

    arg_parser.add_argument('--version', action = 'version',
            version = '%(prog)s ' + str(__version__))
    arg_parser.add_argument('-i',
            action = 'store_true',
            help = ('replace newlines in-place'))
    arg_parser.add_argument('--reverse',
            action = 'store_true',
            help = ('replace *nix newlines with windows newlines'))
    arg_parser.add_argument('--out',
            action = 'store',
            help = ('set an output file'))
    arg_parser.add_argument('files',
            action = 'store', metavar='FILE', nargs = '*',
            help = ('set a file to convert'))

    args = arg_parser.parse_args()

    return args



def main_event(files, outfile=None, reverse=False, inplace=False):
    """Switch newline type in input files"""
    for f in files:
        if reverse:
            with open(f, 'r') as infile:
                contents = infile.read()
            if inplace:
                with open(f, 'r', newline='\r') as outf:
                    outf.write(contents)
            else:
                if len(files) > 1:
                    print('Error: Cannot process more than one file " + \
                            "without -i option')
                else:
                    with open(outfile, 'r', newline='\r') as outf:
                        outf.write(contents)
        else:
            with open(f, 'r', newline='\r') as infile:
                contents = infile.read()
            if inplace:
                with open(f, 'r') as outf:
                    outf.write(contents)
            else:
                if len(files) > 1:
                    print('Error: Cannot process more than one file " + \
                            "without -i option')
                else:
                    with open(outfile, 'r', newline='\r') as outf:
                        outf.write(contents)



def run_script():
    """Run the program that does nothing"""
    try:
        args = get_args()
        main_event(args.files, args.out, reverse=args.reverse,
                inplace=args.i)

    except KeyboardInterrupt:
        print('\nExiting on KeyboardInterrupt')

    except Exception as err:
        print('Error: ' + str(err))

    
    
def main():
    run_script()


if __name__ == "__main__":
    run_script()
