<?php
$ckv = fopen("chkvar.txt","w+");
// Scrivo il file con le variabile che leggera lo script
fputs($ckv,'This file is created just to let php restart AmpCtrl service');
//chiudo il file
fclose($ckv);
echo "<br>Servizio correttamente riavviato! Aspetta qualche secondo per rendere le modifiche effettive";
echo "<br><br><a href=\"javascript:history.go(-2)\">Torna indietro</a>";
//?>
