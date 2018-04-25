# dogoncouch-misc
Miscellany.

## Index
- [Network](network/) - Network related scripts.
  - [ssltest.sh](network/#ssltestsh) - Checks http and ssh protocol security on a remote host.
  - [Reverse Shell](network/#reverse-shell) - Reverse shell server and client.
  - [geofind.py](network/#geofindpy) - Prints GeoIP information on a hostname or IP address.
  - [myip.py](network/#myippy) - Finds and displays your public IP address and (approximate) location via duckduckgo.
  - [putkey.sh](network/#putkeysh) - Adds your ssh public key to `~/.ssh/authorized_keys` on a remote host.
- [uselog.py](uselog/#uselogpy) - Logs system usage statistics to syslog.
- [SIEM testing](siem_testing/) - SIEM testing scripts.
  - [logflood.py](siem_testing/#logfloodpy) - Floods log files using old log events with new date stamps.
  - [wlsim.py](siem_testing/#wlsimpy) - Simulates brute force attacks by repeating the same wordlist.
- [Misc](misc/) - Very miscellaneous.
  - [html-gen.py](misc/#html-genpy) - Creates HTML files for directories full of pictures or other files.
  - [fix-newlines.py](misc/#fix-newlinespy) - Switches newlines in a file between \r and \n.
  - [clean-fixtures.py](misc/#clean-fixturespy) - Removes primary keys from django fixtures.
