from subprocess import run,check_output,PIPE, Popen,call
import datetime


prev_occurances = {}
print('scanning...')

#scan ble
run(args=['sudo', "hciconfig", "hci0", "down"])
run(args=['sudo', "hciconfig", "hci0", "up"])
monitor_proc = Popen(['sudo','hcitool','lescan','--duplicates'], stdout=PIPE)


start_time = datetime.datetime.now()
start_time_actual = start_time
interval = datetime.timedelta(seconds=120)

addr_to_names = {}
prev_occurances = {}
addr_to_occurances = {}

def new_log():
    global addr_to_names
    global addr_to_occurances
    global prev_occurances
    addr_to_names = {}
    prev_occurances = addr_to_occurances
    addr_to_occurances = {}

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

        if(not addr in addr_to_names):
            addr_to_names[addr] = []
            addr_to_occurances[addr] = 0
            
        if(name not in addr_to_names[addr]): addr_to_names[addr].append(name)
        addr_to_occurances[addr] += 1

        #record address to names
        time_recorded = datetime.datetime.now()

        if(time_recorded - start_time > interval):
            #new slice
            start_time = time_recorded
            output("new slice: " + str(start_time))

        for addr in addr_to_names:
            if(len(addr_to_names) > 1):
                output(addr + " has multiple names, this may be indicative of an attack: " + str(addr_to_names))
            if(addr in prev_occurances and prev_occurances[addr] > 0 and addr_to_occurances[addr]/prev_occurances[addr] > 3):
                output(addr + " has has seen a major spike in activity, this may be indicative of an attack: " + prev_occurances[addr] + "->" + addr_to_occurances[addr])

            prev_occurances[addr] = addr_to_occurances[addr]