import os

def checkvol():
    ss=(os.popen('upsd -i').readlines())
    #print ss
    sd=str(ss)
    pos=sd.find('LOW')
    if sd[pos+4] == 'N':
        abc = 1
    else:
        abc = 2
    #abc=sd[14:20]
    #sd.readline()
    #print "w"
    #print "w"
    #print abc
    #print "w"
    #print "w"
    #print sd
    #print "w"
    return abc

    
#checkvol()
              
