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
from argparse import FileType
import os.path


__version__ = '0.1'

# All HTML before identifier:
start_html = """
<head>
    <title>TITLE</title>
</head>
<body>
    <h1>Stuff</h1>
    <p>The identifier is"""

# All HTML after identifier:
end_html = """.</p>
    <p>Have a nice day!</p>
</body>"""

# This will not put a space before or after the identifier.

# Usage example: python html-gen.py -i 123 filename.html


def get_args():
    """Set argument options"""

    arg_parser = ArgumentParser()

    arg_parser.add_argument('--version', action = 'version',
            version = '%(prog)s ' + str(__version__))
    arg_parser.add_argument('-i',
            action = 'store', dest = 'identifier',
            help = ('set the identifier'))
    arg_parser.add_argument('file',
            type = FileType('w'), metavar='FILE',
            help = ('set the output file'))

    args = arg_parser.parse_args()

    return args


def generate_html(identifier):
    """Generate the html"""
    outhtml = start_html + identifier + end_html
    return outhtml


def write_html(outhtml, outfile):
    """Write output html to an open file"""
    outfile.write(outhtml)


def run_script():
    """Run the program"""
    try:
        args = get_args()
        outhtml = generate_html(args.identifier)
        write_html(outhtml, args.file)

    except KeyboardInterrupt:
        print('\nExiting on KeyboardInterrupt')

    except Exception as err:
        print('Error: ' + str(err))

    
    
def main():
    run_script()


if __name__ == "__main__":
    run_script()
