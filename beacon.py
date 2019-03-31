
import argparse
import datetime
from monitor import hci_wrapper
from subprocess import run
from malice import april_fools
import advertise

parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('-a', action="store", dest="advertising_address", help='advertising address (defaults to 01:23:DE:AD:BE:EF)', default="01:23:DE:AD:BE:EF")
parser.add_argument('-i', action="store", dest="interval", help='advertising interval', type=int, default=50)
parser.add_argument('-n', action="store", dest="name", help='device name', default='QuickBeacon')
parser.add_argument('-m', action="store_true", dest="monitor", help='monitor flag', default=False)
parser.add_argument('--APRIL_FOOLS', action="store_true", dest="april_fools", help='joke utility, do not use', default=False)

args = parser.parse_args()

#validation and sanitization
advertising_address = args.advertising_address
name = args.name
interval = args.interval

if args.monitor:
    hci_wrapper.start_scan()
elif args.april_fools:
    april_fools.celebrate(lambda x: advertise.advertise(advertising_address=x, name='APRIL\'S PHONE'))
else:
    advertise.advertise(advertising_address=advertising_address, name=name, interval=interval)

print(datetime.datetime.utcnow().strftime('Advertising started: %B %d %Y - %H:%M:%S'))