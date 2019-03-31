from subprocess import run,check_output,PIPE, Popen,call
import datetime

#takes function with 1 param
def celebrate(on_new_addr):
    #scan ble
    run(args=['sudo', "hciconfig", "hci0", "down"])
    run(args=['sudo', "hciconfig", "hci0", "up"])
    monitor_proc = Popen(['sudo','hcitool','lescan','--duplicates'], stdout=PIPE)

    addresses = {}

    def output(msg):
        print(msg)

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

            if(not addr in addresses):
                on_new_addr(addr)
                addresses[addr] = 1