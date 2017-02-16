#! /bin/sh

sudo rm /var/www/MyScripts/AmpCtrl/chkvar.txt
sleep 1
sudo service AmpCtrl restart
sleep 1
