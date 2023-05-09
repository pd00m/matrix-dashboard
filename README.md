## Raspberry PI initial set up

1. Run Raspberry Pi Imager for PI OS Lite

**The following steps are not necessary. This can be done in the imager configuration settings**

2. Add a blank `ssh` file in the root directory after install
3. Add a new file called `wpa_supplicant.conf` in the root folder with the contents below

```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
}
```

## SSH into your PI

## Installation instructions

(copy and paste the below until a requirements txt is made)
sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
sudo apt install python3-pip
sudo apt-get install git
git clone https://github.com/jh442/matrix-dashboard.git
sudo apt-get install libopenjp2-7
sudo pip install python-dateutil
sudo pip install numpy
sudo apt install libopenblas-dev pkg-config libopenblas-dev
sudo apt install gfortran
sudo pip3 install scipy
sudo pip3 install pyowm
sudo pip3 install websocket_client
sudo pip3 install spotipy
sudo pip3 install garminconnect
sudo pip3 install rgbmatrix
sudo pip install -r requirements.txt

## Create the config.ini file

This must be made in the root of the project for the credentials

1. cat > config.ini and paste your passwords.

**If issues with scipy install, use**
sudo apt update
sudo apt install -y python3-scipy

## clone rgb matrix into dir

1.  git clone https://github.com/hzeller/rpi-rgb-led-matrix.git to download the content into the folder
2.  cd in rpi-rgp-led-matrix
3.  sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
4.  make build-python PYTHON=$(command -v python3)
5.  sudo make install-python PYTHON=$(command -v python3)
6.  Switch off on-board sound (`dtparam=audio=off` in `/boot/config.txt`)
7.  reboot

This might take a couple more steps to get the audio drivers disabled as turning off the config didn't work the first time

Once starting, the last step should be to navigate to the spotify section. It will ask for a URL. Click it, and then paste
the entire URL in the SSH session. This should authenticate the app

On a headless unit with Spotipy, it was needed to leverage the following code

self.auth_manager = spotipy.SpotifyOAuth(
scope=scope, open_browser=False
)
https://github.com/plamere/spotipy/blob/master/examples/headless.py

## To run

1. CD into `/matrix-dashboard/impl`
2. `sudo python3 controller_v3.py`
