import math




def diff(seg, base):

    return [seg[0] - base[0], seg[0] - base[1], seg[1] - base[0],
            seg[1] - base[1], base[0] - seg[0], base[0] - seg[1],
            base[1] - seg[0], base[1] - seg[1]]
            
    

def readSubs(rSet,addr):

    if addr.find(".") is -1:

        return rSet[int(addr)]
    else:
        return readSubs(rSet[addr.find('.')][1],addr[addr.find('.') + 1:])

def buildAnim(rSet,addr, rate):

    if addr.find(".") is -1:

        runtime = rSet[int(addr)][2][2] - rSet[int(addr)][2][1]
        framecount = round(runtime * rate)

        frameset = [str(i) + "/" + str(framecount)
                    for i in range(framecount + 1)]

        rSet = rSet[int(addr)][0] + frameset
        
    else:
        return readSubs(rSet[addr.find('.')][1],addr[addr.find('.') + 1:])
