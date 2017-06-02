#Factal Eqs
import cmath

class Formula(object):

    #Preloaded Formulas
    eqs = [
           lambda z,c,pwr: z[-1] ** pwr + c,                                              #mandel
           lambda z,c,pwr: z[-1].conjugate() ** pwr + c,                                  #mbar
           lambda z,c,pwr: complex(abs(z[-1].real),abs(z[-1].imag)) ** pwr + c,           #bShip,
           lambda z,c,pwr: (z[-1] * z[-2] * c) ** pwr + c,                                #sakura,
           lambda z,c,pwr: cmath.sin(z[-1]) ** pwr + c,                                   #sin,
           lambda z,c,pwr: 1/cmath.cos(z[-1]) ** pwr + c,                                 #sec,
           lambda z,c,pwr: cmath.tan(z[-1]) ** pwr + c,                                   #tan,
           lambda z,c,pwr: cmath.sinh(z[-1]) ** pwr + c,                                  #sinh,
           lambda z,c,pwr: cmath.cosh(z[-1]) ** pwr + c,                                  #sech,
           lambda z,c,pwr: cmath.tanh(z[-1]) ** pwr + c,                                  #tanh,
           lambda z,c,pwr: complex(z[-1].real, abs(z[-1].imag)) ** pwr + c,               #duck,
           lambda z,c,pwr: (c / z[-1]) - z[-1] ** pwr + c,                                #apollyon
           lambda z,c,pwr: z[-1] - 1* (z[-1] ** pwr - 1)/(pwr * z[-1] ** (pwr - 1)) + c,  #nova
           lambda z, c, pwr: (complex(abs(z[-1].real), abs(z[-1].imag))                   #bSaku
                              * complex(abs(c.real), abs(c.imag))
                              * complex(abs(z[-2].real), abs(z[-2].imag))) ** pwr + c,
           lambda z,c,pwr: cmath.log([z[-1],z[-1].conjugate()][z[-1].imag < 0] + c)               #other duck
           ]
    eNames = [
           "Mandelbrot",
           "Mandelbar",
           "Burning Ship",
           "Sakura",
           "Sinebrot",
           "Mandelsec",
           "Tanbrot",
           "Hyperbolic Sinebrot",
           "Hyperbolic Mandelsec",
           "Hyperbolic Tanbrot",
           "Duck Fractal",
           "Apollyon",
           "Broken Nova",
           "Burning Blossom"
           ]

    formula = 0

    def __init__(self,transform=lambda c: c):
        self.transform = staticmethod(transform)

    def __saferEval__(self,s):
        '''Given a string s, checks to make sure it's composed of permitted substrings prior
        to eval.'''

        functions = ["sin","cos","tan","sih","coh","tah","exp","log","asin","acos","atan","phase",
                     "asih","acoh","atah","mean","gmean","hmean","conjugate","abs","fabs","rabs",
                     "iabs","sum","prod","rootx"]

        variables = ["z","c"]

        punctuation = ["+","-","/","*","^"," ","(",")"]

        funct = s

        def sad(arr,s):

            for items in arr:
                while s.find(items) != -1:
                    s = s[:s.find(items)] + s[s.find(items) + len(items):]

            return s

        s = sad(functions,s)
        s = sad(variables,s)
        s = sad(punctuation,s)

        if len(s) == 0: return eval("lambda z,c,pwr:" + funct)
        else:
            print("You're doing something stupid, aren't you?")
            print("Forbidden: ","s")


    def setFormula(self,f): self.formula = f

    def addCustomFormula(self,custom,name):
        #Security Aneurysm Here
        self.eqs += [eval("lambda z,c,p: "+custom)]
        pass

    def read(self,mSet,z,c,pwr,itr,limit):

        '''Generic Fractal ETA.'''
        if not(mSet): z,c = c,z
        z = [z]
        zenith = 1
        i=0

        try:
            c = self.transform.__func__(c)
        except ZeroDivisionError:
            return z # Not like it was going anywhere...

        #NO, REALLY, LETS NOT DIVIDE BY ZERO
        if c == complex(0,0) and pwr < 0: return z

        if pwr < 0:
            z += [c]
            i += 1

        while (abs(zenith) < limit) and i != itr :

            i += 1

            z += [self.eqs[self.formula](z,c,pwr)]
            zenith = z[-1]

        return z #Return coordinate vector of all zs



#This is a fractal formula not currently supported! Don't delete, because
#this points out a flaw in current architecture
#
# #kel
# if i%2== 0: z = z ** pwr + c
# else:
#
#     if i % 3 == 0: z = z ** pwr / c
#     else: z = z ** pwr - c
