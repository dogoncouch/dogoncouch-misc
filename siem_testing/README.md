# dogoncouch-misc/siem\_testing
SIEM testing 

## Index
- [logflood.py](#logfloodpy) - Floods log files using old log events with new date stamps.
- [wlsim.py](#wlsimpy) - Simulates brute force attacks by repeating the same wordlist.

## logflood.py
Floods log files using old log events with new date stamps.

```
usage: logflood.py [-h] [--version] [-m N] [-p N] [-t S.F] FILE [FILE ...]

positional arguments:
  FILE        set a log file to flood

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
  -m N        exit after N events
  -p N        pause every N events (default 100)
  -t S.F      set length of pause in seconds (default 0.1)
```

## wlsim.py
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
