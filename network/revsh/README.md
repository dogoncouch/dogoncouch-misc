# Reverse Shell
Reverse shell server and client.

## revsrv.py
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

## revcli.py
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
