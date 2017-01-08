import os

def checkvol():
<<<<<<< HEAD
    ss=(os.popen('for id in core ; do \
                    echo "$id:\t$(vcgencmd measure_volts $id)"; \
                done').readlines())
    print ss
    sd=str(ss)+"wwwqqq"
    abc=sd[14:20]
=======
    ss=(os.popen('upsd -i').readlines())
    #print ss
    sd=str(ss)
    pos=sd.find('LOW')
    if sd[pos+4] == 'N':
        abc = 1
    else:
        abc = 2
    #abc=sd[14:20]
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
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
              
