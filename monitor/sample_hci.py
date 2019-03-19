from subprocess import run

hci_output=''
while(1) :
    #scan ble
    hci_output = run(args=['sudo', 'timeout','5','hcitool','lescan','--duplicates'])

    addr_to_names = {}
    addr_to_occurances = {}

    if hci_output.stdout:
        #parse input
        for line in hci_output.stdout.splitlines():
            segments = line.split(' ')
            addr = segments[0]
            name = segments[1]

            if(not addr_to_names[addr]):
                addr_to_names[addr] = []
                addr_to_occurances[addr] = 0
                
            if(name not in addr_to_names[addr]): addr_to_names[addr].append(name)

            addr_to_occurances[addr] += 1

        for addr in addr_to_names:
            if(len(addr_to_names) > 1):
                print(addr + " has multiple names, this may be indicative of an attack")



