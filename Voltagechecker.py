import os

def checkvol():
    ss=(os.popen('for id in core ; do \
                    echo "$id:\t$(vcgencmd measure_volts $id)"; \
                done').readlines())
    print ss
    sd=str(ss)+"wwwqqq"
    abc=sd[14:20]
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
              
