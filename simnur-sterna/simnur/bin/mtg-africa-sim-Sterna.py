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

#ftp = FTP('10.100.43.150')
#ftp.login('mtgl2pf','fp2lgtm')
#ftp.cwd('out/L2')
#ftp.dir()
# H:\MMDS\EPSSG-rsa keys\id_rsa_epssgclssftp
# sftp_client = pysftp.Connection(host='vfids.eumetsat.int',username='epssgclssftp',private_key="H:\\MMDS\\EPSSG-rsa keys\\id_rsa_epssgclssftp\\id_rsa_epssgclssftp")
# sftp_client.cwd('in')
# print(sftp_client.listdir())
# localFilePath = '../../Testdata/W_XX-OHB-Stockholm,SAT,AWS1-MWR-1B-RAD_C_OHB__20230816114457_G_D_20240115111111_20240115125434_T_B____.nc'
# remoteFilePath = 'W_XX-OHB-Stockholm,SAT,AWS1-MWR-1B-RAD_C_OHB__20230816114457_G_D_20240115111111_20240115125434_T_B____.nc.tmp'
# sftp_client.put(localFilePath, remoteFilePath)
# sftp_client.cwd('/out')
# localFilePath = '../../Testdata/W_XX-OHB-Stockholm,SAT,AWS1-MWR-00-SRC_C_OHB__20230815055706_G_D_20440115111111_20440115125434_T_B____.nc'
# sftp_client.put(localFilePath, remoteFilePath)
# sftp_client.rename(remoteFilePath, remoteFilePath + ".tmp")
# sftp_client.close()

host='vfids.eumetsat.int'
username='epssgclssftp'
private_key='H:\\MMDS\\EPSSG-rsa keys\\id_rsa_epssgclssftp\\id_rsa_epssgclssftp'

# sink_folder_L0 = '/in'
# sink_folder_L1 = '/out'
sink_folder_L0 = '/out/l0-products'
sink_folder_L1 = '/out/l1-products'
##############################################################################
# Configuration
##############################################################################

# path = '/home/syseng/simulators/mtg/l2pf/testdata/FCI-2-AFRICA/'
# path = '/tcenas/home/neliason/EPSSterna/Testdata' #test data input folder
path = '../../Testdata' #test data input folder
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
    
    # ftp = FTP('10.100.43.150')
    # ftp.login('mtgl2pf','fp2lgtm')
    # ftp.cwd('out/L2')
    # ftp.dir()
    
    sftp_client = pysftp.Connection(host,username,private_key)
       
    rc_start = datetime.now()
    rc_end = rc_start + timedelta(seconds = orbit_length_secs) 
    chunk = 0
    
    # print(os.getcwd())
    os.chdir(path)
    lst = os.listdir('.')
    lst.sort()
    for file1 in lst:
        if file1.endswith(".nc.tmp"):                  
            next_chunk_time = rc_start + timedelta(seconds= (per * chunk))
            while datetime.now() < next_chunk_time:
                time.sleep(1)
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " chunk = " + str(chunk) + " " + file1 + " start sending to FTP")
                logger.info("- chunk = " + str(chunk) + " " + file1 + " start sending to FTP")
                
                # file11 = open(file1, 'rb')
                # ftp.storbinary('STOR '+ file1 + '.tmp', file11)
                # new_file = file1[:-12] + str(i).zfill(4) + file1[-8:]
                # ftp.rename(file1 + '.tmp', new_file)
                # file11.close()
                if "MWR-1B-RAD" in file1:
                    sftp_client.cwd(sink_folder_L1)
                    print(sftp_client.listdir())
                else:
                    sftp_client.cwd(sink_folder_L0)
                    print(sftp_client.listdir())
                sftp_client.put(file1, file1)
                file1_notmp = file1[:-4]
                sftp_client.rename(file1, file1_notmp)
                print(sftp_client.listdir())
                
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " chunk = " + str(chunk) + " " + file1_notmp + " end sending to FTP")
                logger.info("- chunk = " + str(chunk) + " " + file1_notmp + " end sending to FTP")

                chunk += 1
           
    print("=============== Repeat Cycle " + str(i) + " ended =======================")
    logger.info("=============== Repeat Cycle " + str(i) + " ended =====================")
    # ftp.quit()
    # sftp_client.close()
    while datetime.now() < rc_end:
        time.sleep(1)