# AmpCtrl
Electric power consumption monitoring
Sistema di monitoraggio dell'assorbimento elettrico tramite invio di avvisi e allarmi via email. Basato sull'utilizzo di meterN e contatori SDM.

Topic di riferimento: http://www.flanesi.it/forum/viewtopic.php?f=4&t=1916
*******************************************************************************************************************

Per installare:

sudo -s<br>
cd /var/www/MyScripts<br>
git clone https://github.com/amorospo/AmpCtrl.git<br>
mv AmpCtrl/AmpCtrl.service /etc/systemd/system/AmpCtrl.service<br>
chmod -R 755 AmpCtrl<br>
chown -R www-data:www-data AmpCtrl<br>

Una volta installato per prima cosa occorre modificare le variabili a proprio uso e consumo accedendo alla pagina web:<br>
http://localhost/MyScripts/AmpCtrl/Modulo.php<br>
e seguire le istruzioni a video

Successivamente bisogna abilitare e far partire il servizio all'avvio del sistema:

sudo systemctl enable AmpCtrl<br>
sudo systemctl start AmpCtrl<br>

e poi un bel riavvio del sistema (non necessario, giusto per vedere se tutto funziona al riavvio)

shutdown -r now<br>

*******************************************************************************************************************
Al riavvio controlliamo il service se viene caricato e funziona correttamente.

sudo service AmpCtrl status

l'output dovrebbe essere qualcosa del genere:

● AmpCtrl.service - Electric power consumption monitoring<br>
   Loaded: loaded (/etc/systemd/system/AmpCtrl.service; enabled)<br>
   Active: active (running) since lun 2017-02-13 11:03:55 CET; 1s ago<br>
 Main PID: 26322 (StartService.sh)<br>
   CGroup: /system.slice/AmpCtrl.service<br>
           ├─26322 /bin/sh /var/www/MyScripts/AmpCtrl/StartService.sh<br>
           ├─26330 python /var/www/MyScripts/AmpCtrl/ChkVar.py<br>
           └─26331 python /var/www/MyScripts/AmpCtrl/AmpCTRL.py<br>

feb 13 11:03:55 raspberrypi systemd[1]: Started Electric power consumption monitoring.

