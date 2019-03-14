sudo hciconfig 0 reset
sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 11 11 22 22 33 33 44 44 55 55 66 66 77 77 88 88 00 00 00 00 C8 00
sudo btmgmt -i hci0 le on
sudo btmgmt -i hci0 connectable on
sudo btmgmt -i hci0 name MYNAME
sudo btmgmt -i hci0 advertising on
sudo btmgmt -i hci0 power on
