###!/usr/bin/env python2

import os
from ftplib import FTP
from datetime import datetime
from datetime import timedelta
import time

##############################################################################
# Log settings
##############################################################################
### random comment #######

import logging
import logging.handlers as handlers

logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

logHandler = handlers.TimedRotatingFileHandler('../log/idpfi-simulator.log', when='midnight', interval=1)
logHandler.setLevel(logging.INFO)
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


##############################################################################
# FTP settings
##############################################################################

ftp = FTP('10.100.43.150')
ftp.login('mtgidpfi','1fpd1gtm')
ftp.cwd('out/L1')
ftp.dir()

##############################################################################

path = '/home/syseng/simulators/mtg/idpf-i/testdata/FCI-1C-AFRICA/RC'

rc = 1
# 24 hours 6 times same 4h cycle
for j in range(1,7):
# 4 hours test data
# test github line
#for j in range(1,2):
    for i in range(61, 85):
        rc_start = datetime.now()
        rc_end = datetime.now() + timedelta(seconds = 600)
        print("=============== " + str(rc_start) + "  Repeat Cycle " + str(rc) + " started =====================")
        logger.info("=============== " + str(rc_start) +" Repeat Cycle " + str(rc) + " started =====================")     
        chunk = 0
        per = 15
        os.chdir(path+str(i).zfill(3))
        lst = os.listdir('.')
        lst.sort()
        for file1 in lst:
            if file1.endswith(".nc"):     
                next_chunk_time = rc_start + timedelta(seconds= (per * chunk))
                while chunk < 36 and datetime.now() < next_chunk_time:
                    time.sleep(1)
                else:
                    dtnow = datetime.now()
                    print(dtnow.strftime('%Y-%m-%d %H:%M:%S') + " chunk = " + str(chunk) + " " + file1 + " start sending to FTP")
                    logger.info("- chunk = " + str(chunk) + " " + file1 + " start sending to FTP")
                
                    file11 = open(file1, 'rb')
                    ftp.storbinary('STOR '+ file1 + '.tmp', file11)
                    new_file = file1[:-73] + dtnow.strftime('%Y%m%d%H%M%S') + file1[-59:]
                    #new_file = file1
                    ftp.rename(file1 + '.tmp', new_file)
                    file11.close()
                
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " chunk = " + str(chunk) + " " + new_file + " end sending to FTP")
                    logger.info("- chunk = " + str(chunk) + " " + new_file + " end sending to FTP")
                    chunk += 1
           
    
        while datetime.now() < rc_end:
	    time.sleep(1)
        print("=============== " + str(rc_end) + " Repeat Cycle " + str(rc) + " ended =======================")
        logger.info("=============== " + str(rc_end) + " Repeat Cycle " + str(rc) + " ended =====================")
        rc += 1

ftp.quit()
