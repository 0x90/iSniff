iSniff
======

Tiny WiFi sniffer with Scapy for MAC OS X based on http://www.cqure.net/wp/2014/04/scapy-with-wifi-monitor-rfmon-mode-on-os-x/

# Airport

```
#!/bin/sh
CHANNEL=6
sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/sbin/airport
airport sniff $CHANNEL
watch airport -I en1

```

watch airport -I en1


## Installation

Install Xcode and MacPorts first. After that run this command

```
curl -s https://raw.githubusercontent.com/0x90/iSniff/install.sh | sudo sh
```

[Use brew?](http://www.cqure.net/wp/2014/04/scapy-with-wifi-monitor-rfmon-mode-on-os-x/)

## Injection links

http://www.insanelymac.com/forum/topic/292542-airport-pcie-half-mini/

https://github.com/toleda/wireless_half-mini

http://stagingkiller.wordpress.com/2009/06/26/the-definitive-kismac-article/
http://www.tonymacx86.com/network/104850-guide-airport-pcie-half-mini-v2.html

## Broadcom

http://bcmon.blogspot.ru/

## Hardware links

http://trac.kismac-ng.org/wiki/HardwareList


## Usage

To run example execute folowing:
```
./iSniff.py
```

## Misc

Feel free to contribute!