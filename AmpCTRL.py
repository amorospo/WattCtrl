#!/usr/bin/python

# Amperage alarm system 

####################################################################################
#### Author: Alessandro Botta - amorospo@yahoo.it				####
####################################################################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import linecache
import time
import os
from Variabili_AmpCTRL import *

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
        linecache.checkcache(Amp)

#Let MeterN write first data
time.sleep(10)
file_A = linecache.getline(Amp,4)

# Loop starts
while file_A.startswith(met_A) is True:

	# Reading files and data
       	Amp_num = float((linecache.getline(Amp,4)).replace((''.join([met_A,"("]))," ").replace("*A)"," ").strip())
	time.sleep(1)
       	chk()
        time.sleep(1)

	#Routine in case of SWITCH OFF
	if Amp_num <= Sw_Off:
        	msg_sbj = 'SWITCH OFF'		#Email subject
               	msg_obj = ('No current comsumption. Amperage is now: {0:0.1f} Amp'.format(Amp_num))	#Email text
		send_msg()
		while True: 
			if Amp_num <= Sw_Off:
                       		time.sleep(5)
		        	Amp_num = float((linecache.getline(Amp,4)).replace((''.join([met_A,"("]))," ").replace("*A)"," ").strip())
				chk()
			else:
				#routine Power Outage end
				if Amp_num < HiA and Amp_num > LowA:	
		        		msg_sbj = 'SWITCH OFF ALARM ENDS'		#Email subject
                			msg_obj = ('Alarm ends. Power is up! Amperage is now: {0:0.1f} Amp'.format(Amp_num))	#Email text
					send_msg()
					break
				else:
					time.sleep(2)
				       	Amp_num = float((linecache.getline(Amp,4)).replace((''.join([met_A,"("]))," ").replace("*A)"," ").strip())
					chk()
                       	        	break

	#routine Low Amperage alarm
	elif Amp_num > Sw_Off and Amp_num <= LowA:	
        	msg_sbj = 'Amperage anomaly'			#Email subject
               	msg_obj = ('Warning! Amperage is too low : {0:0.1f} Amp'.format(Amp_num))	#Email text
		send_msg()
		while True:
   	   		if Amp_num > Sw_Off and Amp_num <= LowA:				
	               		time.sleep(5)
		        	Amp_num = float((linecache.getline(Amp,4)).replace((''.join([met_A,"("]))," ").replace("*A)"," ").strip())
				chk()
                        else:	
				#routine Low Amperage alarm end
				if Amp_num < HiA and Amp_num > LowA:
                           		msg_sbj = 'Amperage anomaly ends'		#Email subject
                                       	msg_obj = ('Anomaly ends. Amperage is OK: {0:0.1f} Amp'.format(Amp_num))	#Email text
					send_msg()
                              		break
				else:
					time.sleep(2)
				        Amp_num = float((linecache.getline(Amp,4)).replace((''.join([met_A,"("]))," ").replace("*A)"," ").strip())
					chk()
                                       	break
	
	#routine High Amperage alarm
	elif Amp_num >= HiA:
        	msg_sbj = 'Amperage anomaly'			#Email subject
               	msg_obj = ('Warning! Amperage is too high: {0:0.1f} Amp'.format(Amp_num))	#Email text
		send_msg()
		while True:
  			if Amp_num >= HiA:
				time.sleep(5)
		        	Amp_num = float((linecache.getline(Amp,4)).replace((''.join([met_A,"("]))," ").replace("*A)"," ").strip())
				chk()
                        else:
				#routine High Amperage alarm end
				if Amp_num < HiA and Amp_num > LowA:	
                               		msg_sbj = 'Amperage anomaly ends'		#Email subject
             	                    	msg_obj = ('Anomaly ends. Amperage is OK: {0:0.1f} Amp'.format(Amp_num))	#Email text
					send_msg()
                              		break
				else:
					time.sleep(2)
			        	Amp_num = float((linecache.getline(Amp,4)).replace((''.join([met_A,"("]))," ").replace("*A)"," ").strip())
					chk()
	                               	break

	#Routine normal Amperage
	else:	
		time.sleep(lapse)
	       	Amp_num = float((linecache.getline(Amp,4)).replace((''.join([met_A,"("]))," ").replace("*A)"," ").strip())
		chk()

#Routine reading file error
else:	
	msg_sbj = 'Amperage control fatal error'                #Email subject
       	msg_obj = ('Error reading file %s. No usuful data to process' % (Amp))       #Email text
       	send_msg()
	while True:
		if file_A.startswith(met_A) is False:	
			file_A = linecache.getline(Amp,4)
			chk()
    			time.sleep(5)
		else:
			execfile(os.path.realpath(__file__))
