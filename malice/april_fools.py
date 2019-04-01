from subprocess import run,check_output,PIPE, Popen,call
import datetime
import time

#takes function with 1 param
def celebrate(adv_func, n_ident=0, n_total=1, af_test=False):
    addresses = []

    #scan
    Popen("sudo hcitool lescan > out/hci_scan.txt",shell=True)

    #get hci output
    with open('out/hci_scan.txt') as f:
        #parse input
        for line in f.readlines():
            if('Input/output error' in line):
                exit()
            if(not '...' in line): #filtering the first line of output
                segments = line.split(' ')
                addr = segments[0]
                name = segments[1]

                if(name and '(unknown)' in name and not addr in addresses): #this will actually grab everything, TODO: change that
                    addresses.append(addr)
            

    #advertise a chunk
    print("found %d addresses",len(addresses))
    s = int(len(addresses) * n_ident / n_total)
    e = int(len(addresses) * (n_ident+1) / n_total)
    print("BEGIN THE FOOLING: %d,%d" % (s,e))
    for addr in sorted(addresses)[s:e]:
        print("fooling " + addr)
        if not af_test: adv_func(addr)
        time.sleep(1)

    #cleanup
    run(args=['sudo', "hciconfig", "hci0", "down"])
    run(args=['sudo', "hciconfig", "hci0", "up"])