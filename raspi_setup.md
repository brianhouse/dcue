
### login
    ssh raspberrypi.local
    raspberry:pi

### config
    sudo raspi-config
make sure the time is EST
change password
turn on ssh    
turn off boot to desktop
update raspi-config    

### updates
    sudo apt-get update
    sudo apt-get upgrade

### update firmware (radically improves sound quality, though not volume)    
    # as described at http://dbader.org/blog/crackle-free-audio-on-the-raspberry-pi-with-mpd-and-pulseaudio
    # referencing https://github.com/Hexxeh/rpi-update
    sudo apt-get install git-core
    sudo wget https://raw.github.com/Hexxeh/rpi-update/master/rpi-update -O /usr/bin/rpi-update
    sudo chmod +x /usr/bin/rpi-update
    sudo cp /boot/start.elf /boot/start.elf.knowngood       # backup existing
    sudo BRANCH=next rpi-update                             # update it
    sudo reboot
    /opt/vc/bin/vcgencmd version                            # check firmware version

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

### hostname / remote
    sudo nano /etc/hosts
    sudo nano /etc/hostname
    sudo /etc/init.d/hostname.sh
    sudo reboot
change raspberrypi references to desired

    ssh pi@syncbox-1.local

### sound
    sudo nano /etc/modprobe.d/alsa-base.conf
    options snd-usb-audio index=-2          # change to 0
    sudo reboot
    alsamixer

### python
    sudo apt-get install python3-setuptools
    sudo easy_install3 pip
    sudo pip-3.2 install PyYAML

### monit
    sudo apt-get install monit
see monitrc.smp

### mpg123
    sudo apt-get install mpg123

### testing with Granu
- everything plugged into switch, set to dchp
- share internet connection

### shutdown, remember:
    sudo shutdown -h now


### notes
from shawn -- disk will get corrupted after awhile, have to disable writes

create an image: http://smittytone.wordpress.com/2013/09/06/back-up-a-raspberry-pi-sd-card-using-a-mac/

    # be sure you have the right disk!
    diskutil list
    diskutil unmountDisk /dev/disk1
    sudo dd if=/dev/rdisk1 of=~/Desktop/pi.img bs=1m            # note the 'r' prefix


locking:
http://raspberrypi.stackexchange.com/questions/5112/running-on-read-only-sd-card