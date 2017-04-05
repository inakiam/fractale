import Fractale
from cmath import *

##TODO: Fix recRep so there are no garbage tags.

class AnimEq(object):


    def __init__(self):

        self.rSet = []

    def naiveSplit(self,eq):
        '''Non-recursively splits a formula.'''

        eq = eq.replace("^","**").replace("-","+-").replace("(","(+")

        out = [[i,None] for i in eq.split('+')]

        return out
    
    def recursiveRepair(self,eqList):

        hier = 0
        iStart = 0
        subset = False
        firstPS = 0

        for i in range(len(eqList)):

            
            psIndex = eqList[i][0].find('(')
            peIndex = eqList[i][0].find(')')

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
                
                tmp = [i[0] for i in eqList[iStart:i+1]]
                
                tmp[0] = tmp[0][firstPS+1:]
                
                tmp[-1] = tmp[-1][:peIndex]
                
                tmp = '+'.join(tmp)
                

                tmp = recursiveRepair(naiveSplit(tmp))

                eqList[iStart][1] = tmp

                eqList[iStart][0] = eqList[iStart][0][:firstPS + 1] +\
                                 eqList[i][0][peIndex:]

                for j in range(iStart + 1, i + 1):

                    eqList[j][0] = None

        return eqList

    def remN(self,a):
        '''Removes garbage tags created by recursiveRepair.'''

        bothFailed = 0

        while True:

            try: a.remove([None,None])
            except: bothFailed += 1

            try: a.remove(['',None])
            except: bothFailed += 1

            if bothFailed is 2: break

            bothFailed = 0

        for i in range(len(a)):

            if type(a[i][1]) is list:

                a[i][1] = remN(a[i][1])
        return a

    def setEq(self,eq):

        self.eq = eq
        self.rSet = self.remN(self.recursiveRepair(self.naiveSplit(eq)))
        

    def construct(self):
        '''Returns the function provided.'''

        out = ""

        for i in self.rSet:

            if i[1] is None:

                out += i[0] + "+"

            else:

                out += i[0][:i[0].find("(") + 1] + construct(i[1]) + i[0][
                    i[0].find(")"):] + "+"

        return out[:len(out) - 1].replace("+-","-")

    def addAnim(self, anim, addr):

        if addr.find(".") == -1:

            self.rSet[int(addr)] += [anim]
            
        else:
            return addAnim(self.rSet[addr.find('.')][1],anim,addr[addr.find('.')
                                                             + 1:])

    def newTerm(self,location):
        '''Adds a new zero term to the formula.'''

        if addr.find(".") == -1:
            self.rSet += [0,None]

        else:
            return addAnim(self.rSet[addr.find('.')][1],anim,addr[addr.find('.')
                                                             + 1:])

            







#Old stuff, cannibalise as req'd

def parse(trans):
    ##lambda factory for custom transformations

    while trans.find("^") >= 0:

        trans = trans[:trans.find("^")] + "**" + trans[trans.find("^") + 1:]

    return eval("lambda c: " + trans)

a = AnimEq()

a.setEq("x + y(z + c)")

a.construct()

##transform = 0
##
##def animate(runtime, framerate, trans):
##
##    div = runtime * framerate
##
##    for i in range(div + 1):
##
##        transform = parse(str(div - i) + "/" + str(div) + " * c + " + str(i) +
##                      "/" + str(div) + " * " + trans)
##
##        Fractale.calculate(0,2,80,0,(0j),(0+0j),False,100,100,i,transform)


##def custom(trans):
##    ##lambda factory for custom transformations
##
##    baseForm = str(input("Enter Base Formula: ")).lower().split().join()
##    zcp = [True if baseForm.find(key) > -1 for key in ['z','c','p']]
##
##    terms = []
##    #format [(termnum, startpos, endpos, subtermList)] Gen last
##    #by recursion? then, parsing needs to be a subfunction.
##
##    def findTerms(eq):
##
##        eq += "+"
##
##        output = []
##        termNum = 0
##
##        while i < len(eq) - 1:
##            
##            termInfo = []
##
##            termEnd = eq.find("+",i)
##            termStart = eq.find("+",0 if termInfo is [] else termInfo[-1][2])
##
##            paren = eq.find("(",i)
##            
##            endParen = eq.find(")",i)
##
##            if paren is -1 or endParen is -1:
##                print("Parens bad.")
##
##            #if (z + c) or sin(z + c) but not sin(z), forex
##            if paren < termEnd < endParen:
##
##                #Make sure that given "(z + (z + c))"
##                #function recurses w/ "z + (z + c)"
##                #and not "z + (z + c"
##                lP = 0
##                rP = 0
##
##                for i in range(len(eq)):
##
##                    if eq[i] is "(": lP += 1
##                    if eq[i] is ")" rP += 1
##
##                    if lP is rP and lP + rP != 0:
##                        endParen = i
##                       
##                termInfo += [termNum,paren,endParen + 1,
##                             findTerms(eq[paren + 1:endParen])]
##
##            termInfo += [termNum, termStart, termEnd + 1, None]
##
##            i = termEnd if termEnd > endParen else endParen
##        return termInfo
##    
##    def strip(s):
##        while trans.find("^") >= 0:
##
##            trans = trans[:trans.find("^")] + "**" + trans[trans.find("^") + 1:]
##
##    return eval("lambda c: " + trans)
