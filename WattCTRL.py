#!/usr/bin/python

# Electric consumption alarm system 

####################################################################################
#### Author: Alessandro Botta - amorospo@yahoo.it				####
####################################################################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import linecache
import time
import os
from Variabili_WattCTRL import *

def send_msg():
        server = smtplib.SMTP(smtp_S, smtp_P)    
        server.ehlo()
        server.starttls()
        server.login(from_addr, pwd)
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addrs
        msg['Subject'] = "%s - %s" % (site, msg_sbj)              
        msg.attach(MIMEText(msg_obj))
        time.sleep(1)
        server.sendmail(from_addr, to_addrs.split(','), msg.as_string())
        server.quit()
        time.sleep(lapse)                                 

def chk():
        linecache.checkcache(Watt)

#Let MeterN write first data
time.sleep(10)
file_W = linecache.getline(Watt,4)

# Loop starts
while file_W.startswith(met_W) is True:

	# Reading files and data
       	Watt_num = float((linecache.getline(Watt,4)).replace((''.join([met_W,"("]))," ").replace("*W)"," ").strip())
	time.sleep(1)
       	chk()
        time.sleep(1)

	#Routine in case of SWITCH OFF
	if Watt_num <= Sw_Off:
        	msg_sbj = 'SWITCH OFF'		#Email subject
               	msg_obj = ('No current comsumption. wattage is now: {0:0.1f} Watt'.format(Watt_num))	#Email text
		send_msg()
		while True: 
			if Watt_num <= Sw_Off:
                       		time.sleep(5)
		        	Watt_num = float((linecache.getline(Watt,4)).replace((''.join([met_W,"("]))," ").replace("*W)"," ").strip())
				chk()
			else:
				#routine Power Outage end
				if Watt_num < HiW and Watt_num > LowW:	
		        		msg_sbj = 'SWITCH OFF ALARM ENDS'		#Email subject
                			msg_obj = ('Alarm ends. Power is up! wattage is now: {0:0.1f} Watt'.format(Watt_num))	#Email text
					send_msg()
					break
				else:
					time.sleep(2)
				       	Watt_num = float((linecache.getline(Watt,4)).replace((''.join([met_W,"("]))," ").replace("*W)"," ").strip())
					chk()
                       	        	break

	#routine Low wattage alarm
	elif Watt_num > Sw_Off and Watt_num <= LowW:	
        	msg_sbj = 'wattage anomaly'			#Email subject
               	msg_obj = ('Warning! wattage is too low : {0:0.1f} Watt'.format(Watt_num))	#Email text
		send_msg()
		while True:
   	   		if Watt_num > Sw_Off and Watt_num <= LowW:				
	               		time.sleep(5)
		        	Watt_num = float((linecache.getline(Watt,4)).replace((''.join([met_W,"("]))," ").replace("*W)"," ").strip())
				chk()
                        else:	
				#routine Low wattage alarm end
				if Watt_num < HiW and Watt_num > LowW:
                           		msg_sbj = 'wattage anomaly ends'		#Email subject
                                       	msg_obj = ('Anomaly ends. wattage is OK: {0:0.1f} Watt'.format(Watt_num))	#Email text
					send_msg()
                              		break
				else:
					time.sleep(2)
				        Watt_num = float((linecache.getline(Watt,4)).replace((''.join([met_W,"("]))," ").replace("*W)"," ").strip())
					chk()
                                       	break
	
	#routine High wattage alarm
	elif Watt_num >= HiW:
        	msg_sbj = 'wattage anomaly'			#Email subject
               	msg_obj = ('Warning! wattage is too high: {0:0.1f} Watt'.format(Watt_num))	#Email text
		send_msg()
		while True:
  			if Watt_num >= HiW:
				time.sleep(5)
		        	Watt_num = float((linecache.getline(Watt,4)).replace((''.join([met_W,"("]))," ").replace("*W)"," ").strip())
				chk()
                        else:
				#routine High wattage alarm end
				if Watt_num < HiW and Watt_num > LowW:	
                               		msg_sbj = 'wattage anomaly ends'		#Email subject
             	                    	msg_obj = ('Anomaly ends. wattage is OK: {0:0.1f} Watt'.format(Watt_num))	#Email text
					send_msg()
                              		break
				else:
					time.sleep(2)
			        	Watt_num = float((linecache.getline(Watt,4)).replace((''.join([met_W,"("]))," ").replace("*W)"," ").strip())
					chk()
	                               	break

	#Routine normal wattage
	else:	
		time.sleep(lapse)
	       	Watt_num = float((linecache.getline(Watt,4)).replace((''.join([met_W,"("]))," ").replace("*W)"," ").strip())
		chk()

#Routine reading file error
else:	
	msg_sbj = 'wattage control fatal error'                #Email subject
       	msg_obj = ('Error reading file %s. No usuful data to process' % (Watt))       #Email text
       	send_msg()
	while True:
		if file_W.startswith(met_W) is False:	
			file_W = linecache.getline(Watt,4)
			chk()
    			time.sleep(5)
		else:
			execfile(os.path.realpath(__file__))
