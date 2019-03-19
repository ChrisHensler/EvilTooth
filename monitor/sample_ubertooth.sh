echo "Running Ubertooth...to terminate, close this window."
while true; do timeout 120 ubertooth-btle -f -r scans/$(date +%Y_%m_%d__%H_%M_%S).pcap; done