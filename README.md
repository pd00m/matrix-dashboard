sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
sudo apt install python3-pip
sudo apt-get install git
git clone https://github.com/jh442/matrix-dashboard.git
sudo apt-get install libopenjp2-7
sudo pip install python-dateutil
sudo pip install numpy
sudo apt-get install libatlas-base-dev
sudo pip install scipy
sudo pip3 install pyowm
sudo pip3 install websocket_client
sudo pip3 install spotipy
sudo pip3 install garminconnect
sudo pip3 install rgbmatrix
sudo pip install -r requirements.txt

clone rgb matrix into dir
cd in rpi-rgp-led-matrix
sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)
Switch off on-board sound (`dtparam=audio=off` in `/boot/config.txt`)
reboot

On a headless unit with Spotipy, it was needed to leverage the following code

self.auth_manager = spotipy.SpotifyOAuth(
scope=scope, open_browser=False
)
https://github.com/plamere/spotipy/blob/master/examples/headless.py
