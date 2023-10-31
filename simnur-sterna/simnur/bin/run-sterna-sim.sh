#!/bin/bash
  
# Set your SSH key file and passphrase if applicable
SSH_KEY="/tcenas/home/neliason/.ssh/id_rsa_newkey2"


SINK_FOLDER_L0='/out/l0-products/'
SINK_FOLDER_L1='/out/l1-products/'
SINK_FOLDER_TLE='/out/tle-data/'


# Set the remote server information
USERNAME="aws-pfm"
HOST="163.165.213.23"
# PORT="22"  # Default SSH port

# Set the local and remote file paths
L0_1="W_XX-OHB-Stockholm,SAT,AWS1-MWR-00-SRC_C_OHB__20230815055706_G_D_20440115111111_20440115125434_T_B____.nc.tmp"
L0_1_R="W_XX-OHB-Stockholm,SAT,AWS1-MWR-00-SRC_C_OHB__20230815055706_G_D_20440115111111_20440115125434_T_B____.nc"

L0_2="W_XX-OHB-Stockholm,SAT,AWS1-NAV-00-SRC_C_OHB__20230815055706_G_D_20440115111111_20440115125434_T_B____.nc.tmp"
L0_2_R="W_XX-OHB-Stockholm,SAT,AWS1-NAV-00-SRC_C_OHB__20230815055706_G_D_20440115111111_20440115125434_T_B____.nc"

L1="W_XX-OHB-Stockholm,SAT,AWS1-MWR-1B-RAD_C_OHB__20230816114457_G_D_20240115111111_20240115125434_T_B____.nc.tmp"
L1_R="W_XX-OHB-Stockholm,SAT,AWS1-MWR-1B-RAD_C_OHB__20230816114457_G_D_20240115111111_20240115125434_T_B____.nc"

TLE="0X068_20231014002202_TLE.txt.tmp"
TLE_R="0X068_20231014002202_TLE.txt"

date

# Use a here document to provide SFTP commands
#sftp -i "$SSH_KEY" -P "$PORT" "$USERNAME@$HOST" <<EOF
#put "$LOCAL_FILE" "$REMOTE_PATH"

sftp -oIdentityFile="$SSH_KEY" "$USERNAME@$HOST" <<EOF
put "$TLE" "$SINK_FOLDER_TLE"
rename "$SINK_FOLDER_TLE$TLE" "$SINK_FOLDER_TLE$TLE_R"

put "$L0_1" "$SINK_FOLDER_L0"
rename "$SINK_FOLDER_L0$L0_1" "$SINK_FOLDER_L0$L0_1_R"

put "$L0_2" "$SINK_FOLDER_L0"
rename "$SINK_FOLDER_L0$L0_2" "$SINK_FOLDER_L0$L0_2_R"

put "$L1" "$SINK_FOLDER_L1"
rename "$SINK_FOLDER_L1$L1" "$SINK_FOLDER_L1$L1_R"

quit
EOF

date
