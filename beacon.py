
import argparse
import datetime
import time
from monitor import hci_wrapper, ubertooth_wrapper
from subprocess import run
from malice import april_fools
import advertise

parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('-a', action="store", dest="advertising_address", help='advertising address (defaults to 01:23:DE:AD:BE:EF)', default="01:23:DE:AD:BE:EF")
parser.add_argument('-i', action="store", dest="interval", help='advertising interval', type=int, default=50)
parser.add_argument('-n', action="store", dest="name", help='device name', default='QuickBeacon')
parser.add_argument('-m', action="store_true", dest="monitor_hci", help='monitor flag', default=False)
parser.add_argument('-u', action="store_true", dest="monitor_ubertooth", help='monitor flag', default=False)
parser.add_argument('--APRIL_FOOLS', action="store_true", dest="april_fools", help='joke utility, do not use', default=False)
parser.add_argument('--af_num', action="store", dest="af_num", help='april fools id', default='0')
parser.add_argument('--af_total', action="store", dest="af_total", help='april fools total', default='0')
parser.add_argument('--af_test', action="store_true", dest="af_test", help='joke utility, do not use', default=False)
parser.add_argument('--wait', action="store", dest="wait", help='wait a bit before running', default='0')
parser.add_argument('--af_target', action="store", dest="af_target", help='joke utility, do not use', default=None)
args = parser.parse_args()

time.sleep(args.wait)

#validation and sanitization
advertising_address = args.advertising_address
name = args.name
interval = args.interval

if args.monitor_hci:
    hci_wrapper.start_scan()
if args.monitor_ubertooth:
    ubertooth_wrapper.start_scan()
elif args.april_fools:
    april_fools.celebrate(lambda x: advertise.advertise(advertising_address=x, name='APRIL\'S PHONE'), n_ident=args.af_num, n_total=args.af_total, af_test=args.af_test, af_target=args.af_target)
else:
    advertise.advertise(advertising_address=advertising_address, name=name, interval=interval)
    print(datetime.datetime.utcnow().strftime('Advertising started: %B %d %Y - %H:%M:%S'))