import shutil
import os

def usbexport():
    source = os.listdir("/home/pi/Downloads/CRTApp/")
<<<<<<< HEAD
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
        
=======
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
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
