import pyaudio
import binascii

def sendAudio(t,date,time,r,d,s,num):
    if num%60==0:
        try:
            if(t>=0):
                a="1 RRRR + SSSS + DDDD" + "\n" + "2" + date+" +"+time+" +"+t+" Deg C"
            else:
                a="1 RRRR + SSSS + DDDD" + "\n" + "2" + date+" +"+time+" -"+t+" Deg C"
            b = bin(int(binascii.hexlify(c),16))

            sample_stream=[]
            high_note = (b'\xFF'*100 + b'\0'*100)*50
            low_note = (b'\xFF'*50 + b'\0'*50)*100

            for bit in b[2:] :
                if bit == '1':
                    sample_stream.extend(high_note)
                else:
                    sample_stream.extend(low_note)

            sample_buffer = b''.join(sample_stream)

            p = pyaudio.PyAudio()
            stream = p.open(format = p.get_format_from_width(4),channels=1,rate=44100,output=True)
            #stream.write(sample_buffer)   """ ISKO CHALAANE PE INFINITE LOOP AARA HAI AND KUCH HO NHI RAHA!! """
        except:
            pass