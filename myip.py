#!/usr/bin/python3

import urllib.request
import re

con = urllib.request.Request('https://duckduckgo.com/?q=ip')
result = urllib.request.urlopen(con).read()

rex = re.compile(r".*Your IP address is (\d+\.\d+\.\d+\.\d+) " + \
        "in <[^>]+>([^<]+)</a>")

ip = re.findall(rex, str(result))

print('Public IP address: %s' %ip[0][0])
print('Locality: %s' %ip[0][1])
