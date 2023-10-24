#!/usr/bin/env python3

import os
from ftplib import FTP
from datetime import datetime
from datetime import timedelta
import time

##############################################################################
# Log settings
##############################################################################

import logging
import logging.handlers as handlers

logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

logHandler = handlers.TimedRotatingFileHandler('../log/sterna-simulator.log', when='midnight', interval=1)
logHandler.setLevel(logging.INFO)
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


##############################################################################
# FTP settings
##############################################################################

#ftp = FTP('10.100.43.150')
#ftp.login('mtgl2pf','fp2lgtm')
#ftp.cwd('out/L2')
#ftp.dir()

##############################################################################

# path = '/home/syseng/simulators/mtg/l2pf/testdata/FCI-2-AFRICA/'
path = '/tcenas/home/neliason/EPSSterna'
num_of_orbits = 145

for i in range(1, num_of_orbits):
    print("=============== Repeat Cycle " + str(i) + " started =====================")
    logger.info("=============== Repeat Cycle " + str(i) + " started =====================")
    
    ftp = FTP('10.100.43.150')
    ftp.login('mtgl2pf','fp2lgtm')
    ftp.cwd('out/L2')
    ftp.dir()
    
    rc_start = datetime.now()
    rc_end = rc_start + timedelta(seconds = 600) 
    chunk = 0
    per = 270
    os.chdir(path)
    lst = os.listdir('.')
    lst.sort()
    for file1 in lst:
        if file1.endswith(".nc"):     
            next_chunk_time = rc_start + timedelta(seconds= (per * chunk))
            while datetime.now() < next_chunk_time:
                time.sleep(1)
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " chunk = " + str(chunk) + " " + file1 + " start sending to FTP")
                logger.info("- chunk = " + str(chunk) + " " + file1 + " start sending to FTP")
                
                file11 = open(file1, 'rb')
                ftp.storbinary('STOR '+ file1 + '.tmp', file11)
                new_file = file1[:-12] + str(i).zfill(4) + file1[-8:]
                ftp.rename(file1 + '.tmp', new_file)
                file11.close()
                
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " chunk = " + str(chunk) + " " + new_file + " end sending to FTP")
                logger.info("- chunk = " + str(chunk) + " " + new_file + " end sending to FTP")

                chunk += 1
           
    print("=============== Repeat Cycle " + str(i) + " ended =======================")
    logger.info("=============== Repeat Cycle " + str(i) + " ended =====================")
    ftp.quit()
    #time.sleep(600)
    while datetime.now() < rc_end:
        time.sleep(1)

#ftp.quit()
