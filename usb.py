import shutil
import os

def usbexport():
    source = os.listdir("/home/pi/Downloads/CRTApp/")
    destination = "/media/pi/CRTEXPORT"
    #dest2="/media/pi/CRT/testing.text"
    #CHANGE NAME OF TANVI TO CRT AND THE PENDRIVE BEING CONNECTED SHOULD BE NAMED CRT
    try:
        for files in source:
            if files.endswith("testing.text"):
                print "25"
                shutil.move(files,destination)
    except:
        #os.remove(destination)
        print "24"
        shutil.move(files,destination)
#usbexport()        
