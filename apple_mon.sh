#!/bin/sh

CHANNEL=7

sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/sbin/airport
airport sniff $CHANNEL
