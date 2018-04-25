# dogoncouch-misc/network
Network related scripts.

## Index
- [ssltest.sh](#ssltestsh) - Checks http and ssh protocol security on a remote host.
- [Reverse Shell](#reverse-shell) - Reverse shell server and client.
- [geofind.py](#geofindpy) - Prints GeoIP information on a hostname or IP address.
- [myip.py](#myippy) - Finds and displays your public IP address and (approximate) location via duckduckgo.
- [putkey.sh](#putkeysh) - Adds your ssh public key to `~/.ssh/authorized_keys` on a remote host.


## ssltest.sh
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

## Reverse Shell
Reverse shell server and client.

### revsrv.py
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

### revcli.py
Sends a reverse shell to a server running revsrv.py.

```
usage: revcli.py [-h] [--version] [--verbose] [-k] [-r INTERVAL] host port

positional arguments:
  host         set the remote host
  port         set the remote port

optional arguments:
  -h, --help   show this help message and exit
  --version    show program's version number and exit
  --verbose    enable terminal output
  -k           send keepalive packets every 90 seconds
  -r INTERVAL  reconnect interval in minutes (default 5)
```

## geofind.py
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

## myip.py
Finds and displays your public IP address and (approximate) location via duckduckgo.

```
usage: myip.py [-h] [--version]

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

## putkey.sh
Adds your ssh public key to `~/.ssh/authorized_keys` on a remote host.

```
usage: putkey.sh [-hv] [-f KEYFILE] [USER@]HOST
  -h                  Print this help message
  -v                  Print the version number
  -f FILE             Set the key file (default ~/.ssh/id_rsa.pub)
```
