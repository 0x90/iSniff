#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Tiny WiFi iSniff for iDev
#
# Links:
# http://blog.oneiroi.co.uk/hacking/mac/wifi-recon-using-osx-native-tools/
#
# sudo ifconfig en0 ether d4:33:a3:ed:f2:12
# sudo ifconfig en1 Wi-Fi xx:xx:xx:xx:xx:xx

__author__ = '090h'
__license__ = 'GPL'

from sys import exit
from os import geteuid, remove
from glob import glob
from subprocess import Popen
from time import sleep
from signal import SIGHUP
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from scapy.all import *


try:
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler
except ImportError:
    print('Install watchdog with pip:\n\tpip install watchdog')
    exit(0)


class CapHandler(PatternMatchingEventHandler):

    patterns = ["*.cap"]

    def __init__(self, observer):
        super(CapHandler, self).__init__()
        self.observer = observer
        self.cap = None
        self.counter = 0

    def on_created(self, event):
        if not event.is_directory:
        # if not event.is_directory and event.src_path.startswith('airportSniff'):
            print("file created: %s" % event.src_path)
            self.cap = event.src_path
            self.observer.stop()

    # def on_modified(self, event):
    #     if not event.is_directory:
    #         self.counter += 1
    #         print("file modified: %s count: %i" % event.src_path, self.counter)


class iSniff(object):

    airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

    def __init__(self):
        self.observer = None
        self.airport = None
        self.cap = None

    def pkt_handler(self, pkt):
        print(hexdump(pkt))

    def monitor(self, channel, sleep_time=10):
        # Prepare filemon
        self.observer = Observer()
        fhandler = CapHandler(self.observer)
        self.observer.schedule(fhandler, '/tmp', recursive=False)
        self.observer.start()

        # Run airpiort
        self.airport = Popen([self.airport_path, "sniff", str(channel)], close_fds=True)
        print('Waiting for airport to fill aircap')
        sleep(sleep_time)
        self.airport.send_signal(SIGHUP)

        # Get .cap file path and airport PID
        self.cap = fhandler.cap
        print('File catched: %s airport PID: %i' % (self.cap, self.airport.pid))

    def run(self, channel):
        self.monitor(channel)

        # sniff(offline=self.cap, prn=self.pkt_handler, lfilter=lambda x: x.haslayer(Dot11))
        print('Starting sniffer...')
        sniff(offline=self.cap, prn=self.pkt_handler, )

    def stop(self):
        print('Stopping')
        if self.observer is not None:
            self.observer.stop()

        if self.airport is not None:
            print('Killing airport PID: %i' % self.airport.pid)
            self.airport.kill()

    def clear_tmp(self):
        print('Cleaning /tmp...')
        for f in glob('/tmp/airportSniff*.cap'):
            # print('Removing: %s' % f)
            remove(f)



if __name__ == "__main__":
    parser = ArgumentParser(description='iSniff demo', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--channel', type=int, required=True, help='wifi channel')
    parser.add_argument('-C', '--clear', action='store_true', default=False, help='Remove all /tmp/airportSniff*.cap ')
    args = parser.parse_args()

    if geteuid() != 0:
        print("[-] Your have to be root to put your wireless in monitor mode!")
        exit(0)

    print "[*] Starting scan on channel %s" % args.channel
    isniff = iSniff()

    try:
        isniff.run(args.channel)
    except KeyboardInterrupt:
        isniff.stop()
    finally:
        if args.clear:
            isniff.clear_tmp()


 # wlan.fc.type == 0           Management frames
        # wlan.fc.type == 1           Control frames
        # wlan.fc.type == 2           Data frames
        # wlan.fc.type_subtype == 0   Association request
        # wlan.fc.type_subtype == 1   Association response
        # wlan.fc.type_subtype == 2   Reassociation request
        # wlan.fc.type_subtype == 3   Reassociation response
        # wlan.fc.type_subtype == 4   Probe request
        # wlan.fc.type_subtype == 5   Probe response
        # wlan.fc.type_subtype == 8   Beacon
        # if pkt.type == 0 and pkt.subtype == 8:
            #if pkt.addr2 not in ap_list :
            #ap_list.append(pkt.addr2)
            # print "AP MAC: %s with SSID: %s " % (pkt.addr2, pkt.info)


#!/usr/bin/python -tt
import subprocess
airport = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'

def getAirportInfo():
  arguments = [airport,"--getinfo"]
  execute = subprocess.Popen(arguments, stdout=subprocess.PIPE)
  out, err = execute.communicate()
  dict = {}
  for line in out.split('\n'):
    parse = line.split(': ')
    try:
      key = parse[0].strip()
      value = parse[1]
      dict[key] = value
    except IndexError:
      None
  return dict
airportInfo = getAirportInfo()
print airportInfo['SSID']