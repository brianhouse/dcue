
### login
    pi:wavefarm

### config
    sudo raspi-config

### network
    ifconfig
    sudo nano /etc/network/interfaces

    auto lo
     
    iface lo inet loopback
    iface eth0 inet dhcp
     
    allow-hotplug wlan0
    auto wlan0
    face wlan0 inet dhcp
            wpa-ssid "ssid"
            wpa-psk "password"

    sudo ifup wlan0
    ping google.com

### time
    sudo /etc/init.d/ntp status
    ntpq -c rl

### remote
    ssh pi@raspberrypi.local

### python
    sudo apt-get install python3-setuptools
    sudo easy_install3 pip
    sudo pip-3.2 install PyYAML


### testing with Granu
- everything plugged into switch, set to dchp
- share internet connection


### notes

from shawn -- disk will get corrupted after awhile, have to disable writes

do we need an ifup in the cron?