install:
	sudo apt-get update
	sudo apt-get upgrade -y
	sudo apt-get install python-pip -y
	sudo pip install python-uinput
	sudo cp 40-uinput.rules /etc/udev/rules.d
	sudo cp remote.service /etc/systemd/system
	sudo systemctl enable remote.service
	sudo systemctl start remote.service

uninstall:
	sudo systemctl stop remote.service
	sudo systemctl disable remote.service
	sudo rm /etc/systemd/system/remote.service
	sudo rm /etc/udev/rules.d/40-uinput.rules
	sudo pip remove python-uinput
	sudo apt-get remove python-pip -y
