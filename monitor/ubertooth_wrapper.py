from subprocess import run,check_output,PIPE, Popen,call

def start_scan():
    monitor_proc = Popen(['ubertooth-btle', '-f'], stdout=PIPE)

    for monitor_output in iter(monitor_proc.stdout.readline, b''):
        print(monitor_output)