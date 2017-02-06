import os
import shutil


def usbexport():
	if not os.path.isdir("/media/pi/CRTEXPORT"):
		return False

	else:
		source = "/home/pi/Desktop/"
		destination = "/media/pi/CRTEXPORT"
		if os.path.exists("/media/pi/CRTEXPORT/exporting.txt"):
			os.remove("/media/pi/CRTEXPORT/exporting.txt")
		#dest2="/media/pi/CRT/testing.text"
	    #CHANGE NAME OF TANVI TO CRT AND THE PENDRIVE BEING CONNECTED SHOULD BE NAMED CRT
		for filename in os.listdir(source):
			if filename.endswith("exporting.txt"):
				shutil.move(source + filename,destination)
		return True
   
