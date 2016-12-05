import shutil
import os

def usbexport():
    source = os.listdir("/home/pi/Downloads/CRTApp/")
    destination = "/media/pi/TANVI/"
    dest2="/media/pi/TANVI/testing.text"
    #CHANGE NAME OF TANVI TO CRT AND THE PENDRIVE BEING CONNECTED SHOULD BE NAMED CRT
    try:
        for files in source:
            if files.endswith("ing.text"):
                shutil.move(files,destination)
    except:
        os.remove(dest2)
        shutil.move(files,destination)
        
