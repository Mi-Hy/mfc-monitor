### 1️⃣ Adjust time to UTC and enable RTC
- `sudo raspi-config`
- `5 Localisation Options` --> `L2 Timezone` --> `None of the above` --> `UTC`
- Reboot Pi `sudo reboot`

### 2️⃣ Create SSH Key to clone this repository
- On the raspberry pi
	```
	ssh-keygen -t ed25519 -C "jarne.vanmulders@kuleuven.be"
	cat ~/.ssh/id_ed25519.pub
	```
- ENTER 3x
- Add key to github account [online] --> settings --> SSH Key
- Clone repo via SSH

### 5️⃣ Connection with temperature sensors DS18B20
1. Connect D to GPIO4
2. Enable w1-gpio: add `dtoverlay=w1-gpio` with `sudo nano /boot/firmware/config.txt`
3. Reboot `sudo reboot`
4. Activate and test onewire:
	``` 
	sudo modprobe w1-gpio
	sudo modprobe w1-therm
	cd /sys/bus/w1/devices
	ls
	``` 
	If you see the sensor's ID as dir here, all is well. 

### 6️⃣ Install required python packages
Install pip `sudo apt install python3-pip`
```
sudo python3 -m pip install pyyaml --break-system-packages
sudo python3 -m pip install filelock --break-system-packages
sudo python3 -m pip install influxdb_client --break-system-packages
sudo python3 -m pip install flask --break-system-packages
sudo python3 -m pip install psutil --break-system-packages
sudo python3 -m pip install pyserial --break-system-packages
``` 
### 7️⃣ Test all individual scripts
1. Test `system.py`
2. Test `voltages.py`
3. Test `load.py`
4. Test `controller.py`
5. Run services
	1. Copy service files to systemd:
	```
	sudo cp ~/mfc-validation/controller.service /lib/systemd/system/
 	```
 	2. Enable and start services
  	```
   	sudo systemctl enable controller.service
   	sudo systemctl start controller.service
  	```
   	3. Logs
    ```
   	sudo journalctl -u controller.service -f
    ```
