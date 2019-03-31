from subprocess import run,check_output,PIPE, Popen,call
import datetime
import advertise


def celebrate():
    #scan ble
    run(args=['sudo', "hciconfig", "hci0", "down"])
    run(args=['sudo', "hciconfig", "hci0", "up"])
    monitor_proc = Popen(['sudo','hcitool','lescan','--duplicates'], stdout=PIPE)

    addrs = {}

    def output(msg):
        print(msg)

    def advertise(addr):
        advertise.advertise(advertising_address=addr)

    for hci_output in iter(monitor_proc.stdout.readline, b''):
        hci_output = hci_output.decode('utf-8')

        output(hci_output)
        if('Input/output error' in hci_output):
            exit()

        #parse input
        for line in hci_output.splitlines():
            segments = line.split(' ')
            addr = segments[0]
            name = segments[1]

            if(not addr in addrs):
                advertise(addr)
                addr[addr] = 1