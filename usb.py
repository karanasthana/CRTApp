import shutil

def usbexport():
    source = os.listdir("/home/pi/Downloads/CRTApp/")
    destination = "/media/pi/TANVI/"
    #CHANGE NAME OF TANVI TO CRT AND THE PENDRIVE BEING CONNECTED SHOULD BE NAMED CRT
    for files in source:
        if files.endswith("put.text"):
            shutil.move(files,destination)
