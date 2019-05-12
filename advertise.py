from subprocess import run

def advertise(advertising_address='', interval=30, name=None):
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
            if((i-1)%2 == 0):
                s2 += ' '
        return s2[0: 5]

    max_interval = int_to_hexstring(interval+1)
    min_interval = int_to_hexstring(interval)

    print("Advertising Address: %s,\n Min Interval: %s,\nMax Interval: %s\n"%(advertising_address, min_interval, max_interval))

    cmd_args = ['sudo', 'hcitool','-i','hci0','cmd']
    cmd_args.append('0x08')                                     #ogf
    cmd_args.append('0x0006')                                   #ocf
    cmd_args += min_interval.split(' ')[::-1]                                    #min_interval
    cmd_args += max_interval.split(' ')[::-1]                                    #max_interval
    cmd_args += '00'
    cmd_args += '00'
    cmd_args += '00'
    cmd_args += advertising_address.split(':')                  #address
    cmd_args += '01'
    cmd_args += '00'
    run(args=cmd_args)

    #set advertise ##TODO: dissect the command and make more configurable
    run(args="sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 11 11 22 22 33 33 44 44 55 55 66 66 77 77 88 88 00 00 00 00 C8 00".split(' '))

    #run(args=["sudo","btmgmt", "-i", "hci0","le","on"])
    #run(args=["sudo","btmgmt","-i","hci0","connectable","on"])
    if name:
        run(args=["sudo","btmgmt","-i","hci0","name",name]).stdout
    else:
        print("disabling scan because we have no name")
        run(args=["sudo","hciconfig","hci0","noscan"]).stdout

    run(args=["sudo","hciconfig","hci0","leadv","3"]).stdout
    #run(args=["sudo","btmgmt","-i","hci0","advertising","on"]).stdout
    #run(args=["sudo","btmgmt","-i","hci0","power","on"]).stdout