install:
	apt-get update
	apt-get upgrade -y
	apt-get install python-pip cec-utils -y
	pip install python-uinput
	cp 40-uinput.rules /etc/udev/rules.d
	cp remote.service /etc/systemd/system
	mv /home/pi/.emulationstation/es_input.cfg /home/pi/.emulationstation/es_input.cfg.bak
	cp es_input.cfg /home/pi/.emulationstation
	addgroup uinput
	adduser pi uinput
	systemctl enable remote.service
	systemctl start remote.service

uninstall:
	systemctl stop remote.service
	systemctl disable remote.service
	delgroup uinput
	mv /home/pi/.emulationstation/es_input.cfg.bak /home/pi/.emulationstation/es_input.cfg
	rm /etc/systemd/system/remote.service
	rm /etc/udev/rules.d/40-uinput.rules
	pip remove python-uinput
	apt-get remove python-pip cec-utils -y
