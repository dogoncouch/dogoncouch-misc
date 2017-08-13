#!/bin/bash

# Script for setting up Ad-Hoc wifi network on a device

# To Do: get settings from CLI/config file


ifconfig wlan0 down
macchanger -e wlan0
iwconfig wlan0 mode Ad-Hoc
iwconfig wlan0 essid "testing"
iwconfig wlan0 key "s:b#?{c"
iwconfig wlan0 freq "2.462G"

iw dev wlan0 set power_save off

ifconfig wlan0 up

