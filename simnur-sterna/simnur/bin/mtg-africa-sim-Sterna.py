#!/usr/bin/env python3

import os
from ftplib import FTP
from datetime import datetime
from datetime import timedelta
import time
import pysftp

print(os.getcwd())
##############################################################################
# FTP settings
##############################################################################

# host='vfids.eumetsat.int'
# username='epssgclssftp'
# private_key='H:\\MMDS\\EPSSG-rsa keys\\id_rsa_epssgclssftp\\id_rsa_epssgclssftp'

host = '163.165.213.23'
username = 'aws-pfm'
private_key = '../../../.ssh/id_rsa_newkey2'

sink_folder_L0 = '/out/l0-products'
sink_folder_L1 = '/out/l1-products'
sink_folder_tle = '/out/tle-data'

##############################################################################
# Configuration
##############################################################################

testdata_path = '../../Testdata' #test data input folder
log_path = '../log/sterna-simulator.log'
num_of_orbits = 24
orbit_length_secs = 3600 # orbit length in seconds
per = 5 #time gap between pushing 2 files/chunks

##############################################################################
# Log settings
##############################################################################

import logging
import logging.handlers as handlers

logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

logHandler = handlers.TimedRotatingFileHandler(log_path, when='midnight', interval=1)
logHandler.setLevel(logging.INFO)
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


for i in range(1, num_of_orbits):
    print("=============== Repeat Cycle " + str(i) + " started =====================")
    logger.info("=============== Repeat Cycle " + str(i) + " started =====================")
        
    sftp_client = pysftp.Connection(host,username,private_key)
       
    rc_start = datetime.now()
    rc_end = rc_start + timedelta(seconds = orbit_length_secs) 
    chunk = 0
    
    os.chdir(testdata_path)
    lst = os.listdir('.')
    lst.sort()
    for file1 in lst:
        if file1.endswith(".tmp"):                  
            next_chunk_time = rc_start + timedelta(seconds= (per * chunk))
            while datetime.now() < next_chunk_time:
                time.sleep(1)
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " chunk = " + str(chunk) + " " + file1 + " start sending to FTP")
                logger.info("- chunk = " + str(chunk) + " " + file1 + " start sending to FTP")
                if "MWR-1B-RAD" in file1:
                    sftp_client.cwd(sink_folder_L1)
                elif "TLE" in file1:
                    sftp_client.cwd(sink_folder_tle)
                else:
                    sftp_client.cwd(sink_folder_L0)
                sftp_client.put(file1, file1)
                file1_notmp = file1[:-4]
                sftp_client.rename(file1, file1_notmp)
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " chunk = " + str(chunk) + " " + file1_notmp + " end sending to FTP")
                logger.info("- chunk = " + str(chunk) + " " + file1_notmp + " end sending to FTP")
                chunk += 1
           
    print("=============== Repeat Cycle " + str(i) + " ended =======================")
    logger.info("=============== Repeat Cycle " + str(i) + " ended =====================")
    sftp_client.close()
    while datetime.now() < rc_end:
        time.sleep(1)
