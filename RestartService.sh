#! /bin/sh

sudo rm /var/www/MyScripts/WattCtrl/chkvar.txt
sleep 1
sudo service WattCtrl restart
sleep 1
