t1 = "z-z^3"
t2 = "z+(z*z + z)+z"
t3 = "z+sin(z*z + z)+z"
t4 = "z-sin(z*z + z)**2+z"

def readSubs(rSet,addr):

    if addr.find(".") is -1:

        return rSet[int(addr)]
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

                

                

def fndTerms(eq):

    eq += "+"

    output = []
    termNum = 0

    i = 0

    termInfo = None

    while i < len(eq) - 1:
        
        

        termEnd = eq.find("+",i + 1)
        
        if termInfo is None:
            termInfo = []
            termStart = 0
        else:
            termStart = termInfo[-1][2]

        paren = eq.find("(",i)
        
        endParen = eq.find(")",i)

        if not((paren is -1) is  (endParen is -1)):
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
                if eq[i] is ")": rP += 1

                if lP is rP and lP + rP != 0:
                    endParen = i
                   
            termInfo += [[termNum,paren,endParen + 1,
                         findTerms(eq[paren + 1:endParen])]]

        termInfo += [[termNum, termStart, termEnd, None]]

        i = termEnd if termEnd > endParen else endParen
        termNum += 1
    return termInfo



    

    
##a = findTerms(t1)
##b = findTerms(t2)
c = findTerms(t3)
##d = findTerms(t4)

