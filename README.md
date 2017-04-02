# UMS Assignment Downloader

## Overview
Download Student assignemnts from LPU UMS. It is based on command line because some of the modules used here doesn't work in windows. Working very well on linux if all packages are installed.

## Module Requirements
Note: Apply ```sudo``` if required for your system.
You should have some of the linux packages installed which are
- google chrome
- chrome webdriver

To install chrome driver follow the instructions:
```
  sudo apt-get install libxss1 libappindicator1 libindicator7
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

  sudo dpkg -i google-chrome*.deb
  sudo apt-get install -f
 ```
 Now we need to install ```xvfb``` which allows us to run Chrome headlessly
 ```
  sudo apt-get install xvfb
 ```
 Time to install ChromeDrive and make it executable
 ```
  sudo apt-get install unzip

wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
 ```
  Install the python dependencies by running:

```
  pip install -r requirements.txt
```
## How to execute
Download the zip and extract to the location where you want to save all your downloaded assignments. 
Run the below command to start execution process and follow the instructions:
```
  python assignment_downloader.py
  ```
