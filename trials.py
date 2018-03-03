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
from argparse import FileType
import os.path
import collections
from string import digits


__version__ = '0.1'


class TrialsCore:

    def __init__(self):
        """Initialize a program that does something"""

        self.args = None
        self.arg_parser = ArgumentParser()
        self.config = None


    def get_args(self):
        """Set argument options"""

        self.arg_parser.add_argument('--version', action = 'version',
                version = '%(prog)s ' + str(__version__))
        self.arg_parser.add_argument('--startfile',
                action = 'store', default = 'ibexframe.js',
                metavar = 'FILE',
                help = ('set the file to use as header'))
        self.arg_parser.add_argument('--out',
                action = 'store',
                help = ('set the output file'))
        self.arg_parser.add_argument('file',
                action = 'store', metavar = 'FILE',
                help = ('set a tab-delimited file to parse'))

        self.args = self.arg_parser.parse_args()


    def parse_file(self):
        """Parse a file into a list of dictionaries"""
        
        with open(self.args.file, 'r', newline='\r') as f:
            headerfields = f.readline().strip("\r").split("\t")
            datarows = [r.strip("\r") for r in f.readlines()]
        
        #Eliminate blank rows
        newdatarows = []
        for d in datarows:
            if d not in {'', '\n', '\t'}:
                newdatarows.append(d)
        datarows = newdatarows
        
        datafields = [x.split("\t") for x in datarows]
        
        #Eliminate blank header fields
        while '' in headerfields:
            headerfields.remove('')

        headerlist = []
        for f in headerfields:
            if '.' in f:
                if not f.split('.')[0] in headerlist:
                    headerlist.append(f.split('.')[0])
            else:
                if not f in headerlist:
                    headerlist.append(f)

        # Make translator to translate Message1, Message2, etc. to Message
        translator = str.maketrans('', '', digits)

        # Parse rows into dictionaries
        parsedrows = []
        for row in datafields:
            parsedrow = collections.OrderedDict()
            for h in range(len(headerfields)):
                if "." in headerfields[h]:
                    c, o = headerfields[h].split(".")
                    if not c in parsedrow.keys():
                        parsedrow[c] = {}
                    # Convert Question.as1, Question.as2, etc to Question.as list
                    numberset = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
                    if o[-1] in numberset:
                        o = o.translate(translator)
                        if o in parsedrow[c]:
                            parsedrow[c][o].append(row[h])
                        else:
                            parsedrow[c][o] = list(o)
                    else:
                        parsedrow[c][o] = row[h]
                else:
                    if not "identifiers" in parsedrow:
                        parsedrow["identifiers"] = {}
                    parsedrow["identifiers"][headerfields[h]] = row[h]
            parsedrows.append(parsedrow)
        
        # Assemble output
        mainblock = ''
        for row in parsedrows:
            identifiers = row.pop("identifiers")
            rowoutput = "// %s %s%s\n" % (identifiers['label'],
                    identifiers['item'], identifiers['condition'])
            rowoutput += '[["' + identifiers['label'] + \
                    ', ' + identifiers['item'] + '], '
            for k in row.keys():
                # Strip numbers from multiple controller outputs with translate
                # while assembling row output
                rowoutput += str(k).translate(translator) + ': ' + \
                        str(row[k]) + ', '
            rowoutput = rowoutput[:-2]
            rowoutput += '],\n'
            mainblock += rowoutput

        mainblock = mainblock[:-2]

        mainblock += '\n];'

        # Read the header file
        with open(self.args.startfile, 'r') as f:
            header = f.read()

        # Output to file
        with open(self.args.out, 'w') as f:
            f.write(header + '\n' + mainblock[:-2])

        # Fix double-escaped newlines (by cheating):
        #os.system("sed -i 's/\\\\\\\\/\\\\/' " + self.args.out)
        os.system("perl -i -pe 's/\\\\/\\/' " + self.args.out



    def run_script(self):
        """Run the program that does something"""
        try:
            self.get_args()
            self.parse_file()

        except KeyboardInterrupt:
            print('\nExiting on KeyboardInterrupt')

        except Exception as err:
            print('Error: ' + str(err))

    
    
def main():
    thing = TrialsCore()
    thing.run_script()


if __name__ == "__main__":
    thing = TrialsCore()
    thing.run_script()
