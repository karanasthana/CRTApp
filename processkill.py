import os
import psutil
from os import getpid
from sys import argv,exit


def hangproblem():
    for process in psutil.process_iter():
        process_string=str(process)
        name_index=process_string.find('name=')
        process_name=process_string[name_index+6:name_index+13]
        if process_name=='pcmanfm':
            try:
                id_index=process_string.find('pid=')
                process_id=process_string[id_index+4:id_index+8]
                #print bbbb
                #process.terminate()
                process_id_string=str(process_id)
                os.system("kill -9 "+process_id_string)
            except:
                pass
