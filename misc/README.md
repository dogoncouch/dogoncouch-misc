# dogoncouch-misc/misc
Very miscellaneous.

## Index
  - [html-gen.py](#html-genpy) - Creates HTML files for directories full of pictures or other files.
  - [fix-newlines.py](#fix-newlinespy) - Switches newlines in a file between \r and \n.
  - [clean-fixtures.py](#clean-fixturespy) - Removes primary keys from django fixtures.

## html-gen.py
Creates HTML files for directories full of pictures or other files by combining a starter HTML file, the filename, and an ender HTML file. Can also create files one at a time based on CLI input.

```
usage: html-gen.py [-h] [--version] [-i IDENTIFIER] [--jpgdir JPGDIR]
                   [--outdir OUTDIR] [--starthtml FILE] [--endhtml FILE]
                   [FILE]

positional arguments:
  FILE              set the output file

optional arguments:
  -h, --help        show this help message and exit
  --version         show program's version number and exit
  -i IDENTIFIER     set the identifier
  --jpgdir JPGDIR   set a directory for image file input
  --outdir OUTDIR   set a directory for html file output
  --starthtml FILE  set the start HTML file (default: starter.html)
  --endhtml FILE    set the ending HTML file (default: ender.html)
```

## fix-newlines.py
Switches newlines in a file between \r and \n. Mostly written for people who don't have access to GNU sed.

```
usage: fix-newlines.py [-h] [--version] [-i] [--reverse] [--out OUT]
                       [FILE [FILE ...]]

positional arguments:
  FILE        set a file to convert

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
  -i          replace newlines in-place
  --reverse   replace *nix newlines with windows newlines
  --out OUT   set an output file
```

## clean-fixtures.py
Removes primary keys from django fixtures.

```
usage: clean-fixtures.py [-h] [--version] [FILE [FILE ...]]

positional arguments:
  FILE        set a file from which to erase primary keys

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```
