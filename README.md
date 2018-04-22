# dogoncouch-misc
Miscellany

## Index
- [ssltest.sh](#ssltestsh) - Checks http and ssh protocol security on a remote host.
- [geofind.py](#geofindpy) - Prints GeoIP information on a hostname or IP address.
- [Reverse Shell](#reverse-shell) - Reverse shell server and client.
- [wlsim.py](#wlsimpy) - Simulates brute force attacks by repeating the same wordlist.
- [uselog.py](#uselogpy) - Logs system usage statistics to syslog.
- [myip.py](#myippy) - Finds and displays your public IP address and (approximate) location via duckduckgo.
- [putkey.sh](#putkeysh) - Adds your ssh public key to `~/.ssh/authorized_keys` on a remote host.
- [html-gen.py](#html-genpy) - Creates HTML files for directories full of pictures or other files
- [fix-newlines.py](#fix-newlinespy) - Switches newlines in a file between \r and \n.
- [clean-fixtures.py](#clean-fixturespy) - Removes primary keys from django fixtures.

## Scripts

### ssltest.sh
Checks http and ssh protocol security on a remote host.

```
usage: ssltest.sh [-hv] [options...] HOST
  -h                  Print this help message
  -v                  Print the version number
  -f                  Full ssl certificate check
  -i                  Accept untrusted certificates
  -l                  Use color output for light background
  -c CERTFILE         Set a CA certificate for verification
  -o 'CURLOPTS'       Set additional options for curl
  -p PORT             Set SSH port
  -s PORT             Set HTTPS port
```

### geofind.py
Prints GeoIP information on a hostname or IP address. Requirements: geoip-python.

```
usage: geofind.py [-h] [--version] [-f] [--data DATA] [HOST [HOST ...]]

positional arguments:
  HOST         set a host to look up

optional arguments:
  -h, --help   show this help message and exit
  --version    show program's version number and exit
  -f, --full   get full GeoIP output
  --data DATA  set the .dat file to use
```

### Reverse Shell
Reverse shell server and client.

#### revsrv.py
Listens for an incoming reverse shell from a client running revcli.py.

```
usage: revsrv.py [-h] [--version] [-f] port

positional arguments:
  port        set the local port

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
  -f          bind to sockets that are already in use
```

#### revcli.py
Sends a reverse shell to a server running revsrv.py.

```
usage: revcli.py [-h] [--version] [--verbose] host port

positional arguments:
  host        set the remote host
  port        set the remote port

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
  --verbose   enable terminal output
  -k          send keepalive packets every 90 seconds
```

### wlsim.py
Simulates brute force attacks by repeating the same wordlist.

```
usage: wlsim.py [-h] [--version] [-n TRIES] [--file FILE] [--hydra-args HARGS]
                [--generate] [--user USER] [--service SERVICE]
                [HOST [HOST ...]]

positional arguments:
  HOST                set the target host

optional arguments:
  -h, --help          show this help message and exit
  --version           show program's version number and exit
  -n TRIES            set the number of passwords to check
  --file FILE         set the wordlist file
  --hydra-args HARGS  pass additional arguments to hydra
  --generate          generate a random wordlist to use
  --user USER         set the username to use (default: root)
  --service SERVICE   set the service to target (default: ssh)
```

### uselog.py
Logs system usage statistics to syslog (CPU usage, memory usage, CPU temperature). Requirements: psutil.

```
usage: uselog.py [-h] [--version] [--interval INTERVAL] [--facility FACILITY]
                 [--fahr] [--notemp] [--tempfile TEMPFILE]

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  --interval INTERVAL  set logging interval in seconds (default 60)
  --facility FACILITY  set logging facility (local0-7, default local1)
  --fahr               display temperature in Fahrenheit
  --notemp             do not log CPU temperature
  --tempfile TEMPFILE  set a file for temperature readings
```

### myip.py
Finds and displays your public IP address and (approximate) location via duckduckgo.

```
usage: myip.py [-h] [--version]

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

### putkey.sh
Adds your ssh public key to `~/.ssh/authorized_keys` on a remote host.

```
usage: putkey.sh [-hv] [-f KEYFILE] [USER@]HOST
  -h                  Print this help message
  -v                  Print the version number
  -f FILE             Set the key file (default ~/.ssh/id_rsa.pub)
```

### html-gen.py
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

### fix-newlines.py
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

### clean-fixtures.py
Removes primary keys from django fixtures.

```
usage: clean-fixtures.py [-h] [--version] [FILE [FILE ...]]

positional arguments:
  FILE        set a file from which to erase primary keys

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

## Skeleton scripts
Script templates that do nothing really well.

### skeleton/oo.py
Blank object oriented script.

### skeleton/functional.py
Blank functional script.

