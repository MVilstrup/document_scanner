#!/bin/sh
sudo apt-get gedit -y

wget http://python-tesseract.googlecode.com/files/python-tesseract_0.7-1.4_amd64.deb
wget http://python-tesseract.googlecode.com/files/python-tesseract_0.7-1.4_i386.deb
sudo apt-get install tesseract-ocr -y
sudo dpkg -i python-tesseract*.deb
sudo apt-get -f install -y

rm python-tesseract_0.7-1.4_amd64.deb
rm python-tesseract_0.7-1.4_i386.deb

sudo cp /vagrant/tessdata/* /usr/share/tesseract-ocr/tessdata/
sudo apt-get install shotwell vlc -y
sudo apt-get install python-pip -y