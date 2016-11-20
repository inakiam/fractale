import Fractale
from cmath import *

class Anyme(object):

    

def parse(trans):
    ##lambda factory for custom transformations

    while trans.find("^") >= 0:

        trans = trans[:trans.find("^")] + "**" + trans[trans.find("^") + 1:]

    return eval("lambda c: " + trans)

transform = 0

def animate(runtime, framerate, trans):

    div = runtime * framerate

    for i in range(div + 1):

        transform = parse(str(div - i) + "/" + str(div) + " * c + " + str(i) +
                      "/" + str(div) + " * " + trans)

        Fractale.calculate(0,2,80,0,(0j),(0+0j),False,100,100,i,transform)


def custom(trans):
    ##lambda factory for custom transformations

    baseForm = str(input("Enter Base Formula: ")).lower().split().join()
    zcp = [True if baseForm.find(key) > -1 for key in ['z','c','p']]

    terms = []
    #format [(termnum, startpos, endpos, subtermList)] Gen last
    #by recursion? then, parsing needs to be a subfunction.

    def findTerms(eq):

        eq += "+"

        output = []
        termNum = 0

        while i < len(eq) - 1:
            
            termInfo = []

            termEnd = eq.find("+",i)
            termStart = eq.find("+",0 if termInfo is [] else termInfo[-1][2])

            paren = eq.find("(",i)
            
            endParen = eq.find(")",i)

            if paren is -1 or endParen is -1:
                print("Parens bad.")

            #if (z + c) or sin(z + c) but not sin(z), forex
            if paren < termEnd < endParen:

                #Make sure that given "(z + (z + c))"
                #function recurses w/ "z + (z + c)"
                #and not "z + (z + c"
                lP = 0
                rP = 0

                for i in range(len(eq)):

                    if eq[i] is "(": lP += 1
                    if eq[i] is ")" rP += 1

                    if lP is rP and lP + rP != 0:
                        endParen = i
                       
                termInfo += [termNum,paren,endParen + 1,
                             findTerms(eq[paren + 1:endParen])]

            termInfo += [termNum, termStart, termEnd + 1, None]

            i = termEnd if termEnd > endParen else endParen
        return termInfo
    
    def strip(s):
        while trans.find("^") >= 0:

            trans = trans[:trans.find("^")] + "**" + trans[trans.find("^") + 1:]

    return eval("lambda c: " + trans)
