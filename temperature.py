import os
import glob

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir='/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-000001d399e1')[0]
device_file = device_folder+'/w1_slave'


def read_temp_raw():
    f=open(device_file,'r')
    lines=f.readlines()
    f.close()
    return lines

def read_temp():
    lines=read_temp_raw()
    while lines[0].strip()[-3:]!='YES' :
        lines=read_temp_raw()
    check_connection=lines[1]
    check_connection2=check_connection[:8]
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c=float(temp_string)/1000.0
        temp_c = ("%04.1f" % (float(temp_string)/1000.0))
        """print temp_c"""
        temp_c2=float(temp_c)
        if temp_c2<0:
            temp_c = ("%05.1f" % (temp_c2))
            """print temp_c"""


    return temp_c,check_connection2
