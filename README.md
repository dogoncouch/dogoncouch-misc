# dogoncouch-misc
Miscellany

## Scripts

### geofind.py

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
Adds your ssh rsa public key to `authorized_keys` on a remote host.

```
usage: putkey.sh HOST
```

### uselog.py
Logs system statistics to syslog every 20 minutes (local1.info).

```
usage: uselog.py
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

## Skeleton scripts
Script templates that do nothing really well.

### skeleton/oo.py
Blank object oriented script.

### skeleton/functional.py
Blank functional script.

