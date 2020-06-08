# Install the required dependencies
sudo apt-get install -y python3-pip python3-dev
sudo pip3 install -r ./requirements.txt

# Create the service
sudo cp busylight.service /etc/systemd/system/busylight.service
sudo systemctl enable busylight.service
sudo systemctl start busylight.service

# Change permissions of the start up script
sudo chmod +x ./start.sh