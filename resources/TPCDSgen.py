#!/usr/bin/python
"""
This UDF generates k-th part of n part TPCDS generartion. This uses dsdgen and runs it parallelly and uploads the output to HDFS.
It requires following files to be added using "ADD FILE" syntax to the session.
- dsdgen
- tpcds.idx

"""

import argparse
import subprocess
import sys
import os
import time
import random

HDFS_CMD = "hdfs dfs"

def usage():
    print(__file__)

def generate_data_to_hdfs(hdfs_output, partition, scale_factor, num_parts):
    """Generate data using dsdgen and upload it to HDFS."""

    execute("./dsdgen -dir . -force Y -scale %d -child %d -parallel %d" % (scale_factor, partition, num_parts))

    dim_tables=["call_center","catalog_page","date_dim","household_demographics","income_band","item","promotion","reason","ship_mode","store","time_dim","warehouse","web_page","web_site"]
    if partition == 1:
        for d in dim_tables:
            copy_table_to_hdfs(hdfs_output,d,partition,num_parts)

    tables=["catalog_returns","catalog_sales","inventory","store_returns","store_sales","web_sales","web_returns","customer", "customer_demographics","customer_address"]
    for t in tables:
        copy_table_to_hdfs(hdfs_output,t,partition,num_parts)

def copy_table_to_hdfs(hdfs_output, table_name, partition,num_parts):
    local_file_name = "%s_%s_%s.dat" % (table_name,partition,num_parts)
    hdfs_file_name = "%s/%s/%s" % (hdfs_output, table_name, local_file_name)
    execute("%s -mkdir -p %s/%s" % (HDFS_CMD, hdfs_output, table_name))
    execute("%s -copyFromLocal -f %s %s" % (HDFS_CMD, local_file_name, hdfs_file_name))
    os.remove(local_file_name)

def execute(cmd,retry=10):
    if(retry<0):
        sys.exit(1)

    try:
        subprocess.check_call(cmd,stdin=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    except:
        time.sleep(retry*random.randint(retry*60,600))
        execute(cmd,retry-1)


def main():
    parser = argparse.ArgumentParser(description='Generate TPCDS data in parallel')
    parser.add_argument('-s','--scale', metavar='SCALE_FACTOR',type=int, required=True,
                    help='scale factor for TPCDS datagen')
    parser.add_argument('-o','--output', metavar='OUTPUT_HDFS_PATH', required=True,
                    help='HDFS path where the generated data will be stored')
    parser.add_argument('-n','--num_parts', metavar='NUM_PARTS', type=int, required=True,
                    help='Number of parts to divide the datagen')

    args = parser.parse_args()
    partition = None

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        try:
            partition = int(line.strip())
        except:
            print("UDF expects a number as input.")

        if (args.output is None or partition is None or
            args.num_parts is None or args.scale is None):
            usage()
            sys.exit()

        generate_data_to_hdfs(args.output, partition, args.scale, args.num_parts)

if __name__ == "__main__":
    main()
