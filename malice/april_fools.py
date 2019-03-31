from subprocess import run,check_output,PIPE, Popen,call
import datetime

#takes function with 1 param
def celebrate(adv_func, n_ident=0, n_total=1):
    #scan ble
    run(args=['sudo', "hciconfig", "hci0", "down"])
    run(args=['sudo', "hciconfig", "hci0", "up"])
    monitor_proc = Popen(['sudo','hcitool','lescan'], stdout=PIPE)

    start_time = datetime.datetime.now()
    timeout = datetime.timedelta(seconds=8)

    addresses = []

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

        if(name and not '(unknown)' in name)
            addresses.append(addresses)

        if(datetime.datetime.now() - start_time > timeout):
            break

    #advertise a chunk
    s = len(addresses) * n_ident / n_total
    e = len(addresses) * (n_ident+1) / n_total
    for addr in sorted(addresses)[s:e]:
        print("fooling " + addr)
        adv_func(addr)