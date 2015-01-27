#!/bin/sh
sudo apt-get python-support libleptonica -y

wget http://python-tesseract.googlecode.com/files/python-tesseract_0.7-1.4_amd64.deb
wget http://python-tesseract.googlecode.com/files/python-tesseract_0.7-1.4_i386.deb
sudo apt-get install tesseract-ocr -y
sudo dpkg -i python-tesseract*.deb
sudo apt-get -f install -y

rm python-tesseract_0.7-1.4_amd64.deb
rm python-tesseract_0.7-1.4_i386.deb

sudo cp /vagrant/tessdata/* /usr/share/tesseract-ocr/tessdata/

sudo apt-get install libicu-dev -y
sudo apt-get install libpango1.0-dev -y
sudo apt-get install libcairo2-dev -y
