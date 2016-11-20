t1 = "z-z^3"
t2 = "z+(z*z + z)+z"
t3 = "z+sin(z*z + z)+z"
t4 = "z-sin(z*z + z)**2+z"

from graph import Graph
import math

def q(rdepth):

    if rdepth > 0:
        return q(rdepth-1) + q(rdepth-1)
    else:
        return 1

def statout():

    area = Graph()
    classes = [0 for i in range(2**0 + 1)]
    res = 3

    area.updateRes(res,res)

    for yc in range(res):

        for xc in range(res):

            n = area.posX**2 + area.posY**2

            if n > 4:
                classes[0] += 1
            else: classes[1] += 1

            area.posX += area.fsX
        area.posX = area.reset[0]
        area.posY += area.fsY
        if yc % 1000 == 0: print(yc)
    return classes

            
a = math.pi * 4
soe = statout()
err = a - (soe[1]/soe[0] * 4)
    




def numframes(l,rate):

    return 0

def construct(rSet):

    out = ""

    for i in rSet:

        if i[1] is None:

            out += i[0] + "+"

        else:

            

            out += i[0][:i[0].find("(") + 1] + construct(i[1]) + i[0][
                i[0].find(")"):] + "+"

    return out[:len(out) - 1].replace("+-","-")


def addAnim(rSet, anim, addr):

    if addr.find(".") is -1:

        if len(rSet[int(addr)]) is 2:
               rSet[int(addr)] += []

        rSet[int(addr)][2] += [anim]
        
    else:
        return addAnim(rSet[addr.find('.')][1],anim,addr[addr.find('.') + 1:])
    

def readSubs(rSet,addr):

    if addr.find(".") is -1:

        return rSet[int(addr)]
    else:
        return readSubs(rSet[addr.find('.')][1],addr[addr.find('.') + 1:])

def buildAnim(rSet,addr, rate):

    if addr.find(".") is -1:

        runtime = rSet[int(addr)][2][2] - rSet[int(addr)][2][1]
        framecount = round(runtime * rate)

        frameset = [str(i) + "/" + str(framecount) for i in range(framecount + 1)]

        rSet = rSet[int(addr)][0] + frameset
        
    else:
        return readSubs(rSet[addr.find('.')][1],addr[addr.find('.') + 1:])
    
def findTerms(eq):    

    eq = eq.replace("^","**").replace("-","+-")

    out = [[i,None] for i in eq.split('+')]

    def unfuck(a):

        hier = 0
        iStart = 0
        subset = False
        firstPS = 0

        for i in range(len(a)):

            
            psIndex = a[i][0].find('(')
            peIndex = a[i][0].find(')')

            if psIndex != -1:

                if subset == False:
                    iStart = i
                    firstPS = psIndex
                    subset = True

                hier += 1

            if peIndex != -1:

                hier -= 1

            if hier == 0 and subset:
                subset = False
                
                tmp = [i[0] for i in a[iStart:i+1]]
                
                tmp[0] = tmp[0][firstPS+1:]
                
                tmp[-1] = tmp[-1][:peIndex]
                
                tmp = '+'.join(tmp)

                

                tmp = findTerms(tmp)

                a[iStart][1] = tmp

                a[iStart][0] = a[iStart][0][:firstPS + 1] +\
                                 a[i][0][peIndex:]

                for j in range(iStart + 1, i + 1):

                    a[j][0] = None
        
        return a

    def remN(a):

        while True:

            try: a.remove([None,None])
            except: break

        for i in range(len(a)):

            if type(a[i][1]) is list:

                a[i][1] = remN(a[i][1])
        return a

    return remN(unfuck(out))


##def writeTerms(terms):
##
##    out = []
##
##    for term in terms:
##
##        if term
##
##        

                

                

##def fndTerms(eq):
##
##    eq += "+"
##
##    output = []
##    termNum = 0
##
##    i = 0
##
##    termInfo = None
##
##    while i < len(eq) - 1:
##        
##        
##
##        termEnd = eq.find("+",i + 1)
##        
##        if termInfo is None:
##            termInfo = []
##            termStart = 0
##        else:
##            termStart = termInfo[-1][2]
##
##        paren = eq.find("(",i)
##        
##        endParen = eq.find(")",i)
##
##        if not((paren is -1) is  (endParen is -1)):
##            print("Parens bad.")
##
##        #if (z + c) or sin(z + c) but not sin(z), forex
##        if paren < termEnd < endParen:
##
##            #Make sure that given "(z + (z + c))"
##            #function recurses w/ "z + (z + c)"
##            #and not "z + (z + c"
##            lP = 0
##            rP = 0
##
##            for i in range(len(eq)):
##
##                if eq[i] is "(": lP += 1
##                if eq[i] is ")": rP += 1
##
##                if lP is rP and lP + rP != 0:
##                    endParen = i
##                   
##            termInfo += [[termNum,paren,endParen + 1,
##                         findTerms(eq[paren + 1:endParen])]]
##
##        termInfo += [[termNum, termStart, termEnd, None]]
##
##        i = termEnd if termEnd > endParen else endParen
##        termNum += 1
##    return termInfo
##


    

    
a = findTerms(t1)
b = findTerms(t2)
c = findTerms(t3)
d = findTerms(t4)

