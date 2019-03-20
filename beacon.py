
import argparse
import datetime
from subprocess import run

parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('-a', action="store", dest="advertising_address", help='advertising address (defaults to 01:23:DE:AD:BE:EF)', default="01:23:DE:AD:BE:EF")
parser.add_argument('-i', action="store", dest="interval", help='advertising interval', type=int, default=10)
parser.add_argument('-n', action="store", dest="name", help='device name', default='')

args = parser.parse_args()


#validation and sanitization
advertising_address = args.advertising_address
name = args.name
interval = args.interval

#set addr
run(args=['sudo', 'bdaddr',advertising_address])

#reset bluetooth (needs to happen after addr set)
run(args=['sudo', 'hciconfig','0','reset'])

#set advertising frequency
def int_to_hexstring(i):
    s1 = "{:04x}".format(i)
    s2=""
    for i in range(0,len(s1)):
        s2 += s1[i]
        if(i%2 == 0):
            s2 += ' '
    return s2[0: 5]


max_interval = int_to_hexstring(interval+1).split(' ')
min_interval = int_to_hexstring(interval).split(' ')

print("Advertising Address: %s,\n Min Interval: %s,\nMax Interval: %s\n"%(advertising_address, min_interval, max_interval))

cmd_args = ['sudo', 'hcitool','-i','hci0','cmd']
cmd_args.append('0x08')                                     #ogf
cmd_args.append('0x0006')                                   #ocf
cmd_args += min_interval                                    #min_interval
cmd_args += max_interval                                    #max_interval
cmd_args += '00'
cmd_args += '00'
cmd_args += '00'
cmd_args += advertising_address.split(':')                  #address
cmd_args += '01'
cmd_args += '00'
print(run(args=cmd_args))

#set advertise ##TODO: dissect the command and make more configurable
print(run(args="sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 11 11 22 22 33 33 44 44 55 55 66 66 77 77 88 88 00 00 00 00 C8 00".split(' ')))

print(run(args=["sudo","btmgmt", "-i", "hci0","le","on"]).stdout)
print(run(args=["sudo","btmgmt","-i","hci0","connectable","on"]).stdout)
print(run(args=["sudo","btmgmt","-i","hci0",name]).stdout)
print(run(args=["sudo","btmgmt","-i","hci0","advertising","on"]).stdout)
print(run(args=["sudo","btmgmt","-i","hci0","power","on"]).stdout)

print(datetime.datetime.utcnow().strftime('Advertising started: %B %d %Y - %H:%M:%S'))