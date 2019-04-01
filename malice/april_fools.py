from subprocess import run,check_output,PIPE, Popen,call
import datetime
import time

#takes function with 1 param
def celebrate(adv_func, n_ident=0, n_total=1):
    addresses = []

    #get hci output
    with open('out/hci_scan.txt') as f:
        #parse input
        for line in f.readlines():
            if('Input/output error' in line):
                exit()

            segments = line.split(' ')
            addr = segments[0]
            name = segments[1]

            if(name and not '(unknown)' in name and not addr in addresses):
                addresses.append(addr)
            

    #advertise a chunk
    print("found %d addresses",len(addresses))
    print("BEGIN THE FOOLING")
    s = int(len(addresses) * n_ident / n_total)
    e = int(len(addresses) * (n_ident+1) / n_total)
    for addr in sorted(addresses)[s:e]:
        print("fooling " + addr)
        adv_func(addr)