# dogoncouch-misc/uselog
Logs system usage statistics to syslog.

## uselog.py
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
