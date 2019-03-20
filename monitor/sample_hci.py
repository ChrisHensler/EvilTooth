from subprocess import run
import datetime

hci_output=''
prev_occurances = {}
while(1) :
    #scan ble
    run(args=["hciconfig", "hci0", "down"])
    run(args=["hciconfig", "hci0", "up"])
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


        #record address to names
        time_recorded = datetime.datetime.now()
        for addr in addr_to_names:
            with open("scans/names" + addr + ".txt") as f_name:
                with open("scans/occurances" + addr + ".txt") as f_occur:
                    f_name.write("%s\t%s", time_recorded, len(addr_to_names))
                    f_occur.write("%s\t%s", time_recorded, addr_to_occurances[addr])

                    if(len(addr_to_names) > 1):
                        print(addr + " has multiple names, this may be indicative of an attack")

                    if addr_to_occurances[addr]/prev_occurances[addr] > 3:
                        print(addr + " has has seen a major spike in activity, this may be indicative of an attack")

                    prev_occurances[addr] = addr_to_occurances[addr]


                



