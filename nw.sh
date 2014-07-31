#!/bin/bash

AIRPORT="en1"; #may be en0, use networksetup -listallhardwareports to check
WIFI_NETWORK_NAME="network-name"
WIFI_PASSWORD="password"

networksetup -setairportpower $AIRPORT off
networksetup -setairportpower $AIRPORT on
sleep 2

if networksetup -getairportnetwork $AIRPORT | grep -i -a $WIFI_NETWORK_NAME ;
then
    echo 'Connected!';
    exit 0
fi

if networksetup -setairportnetwork $AIRPORT $WIFI_NETWORK_NAME $WIFI_PASSWORD | grep -i -a "Failed" ;
then
    echo 'Failed to connect, just restarting...';
    networksetup -setairportpower $AIRPORT off
    networksetup -setairportpower $AIRPORT on
    sleep 1
fi

networksetup -getairportnetwork $AIRPORT

exit 0;