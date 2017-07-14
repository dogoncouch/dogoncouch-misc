#!/bin/bash

ifconfig wlan0 down
macchanger -e wlan0
iwconfig wlan0 mode Ad-Hoc
iwconfig wlan0 essid "testing"
iwconfig wlan0 key "s:b#?{c"
iwconfig wlan0 freq "2.462G"
ifconfig wlan0 up

