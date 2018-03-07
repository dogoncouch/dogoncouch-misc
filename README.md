# dogoncouch-misc
Miscellany

## Scripts

### geofind.py
Requirements: geoip-python

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

### myip.py
Finds and displays your public IP address via duckduckgo.

```
usage: myip.py
```

### putkey.sh
Adds your ssh public key to `~/.ssh/authorized_keys` on a remote host.

```
Usage: putkey.sh [-hv] [-f KEYFILE] [USER@]HOST
  -h                  Print this help message
  -v                  Print the version number
  -f FILE             Set the key file (default ~/.ssh/id_rsa.pub)
```

### uselog.py
Logs system statistics to syslog (CPU usage, memory usage, CPU temperature).

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

## Skeleton scripts
Script templates that do nothing really well.

### skeleton/oo.py
Blank object oriented script.

### skeleton/functional.py
Blank functional script.

