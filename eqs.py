#Factal Eqs


def mandelbrot(z,c,pwr,itr,limit,j = False,ex = False,i=0,transform=None):

    '''Mandelbrot/Julia ETA.'''

    z = [0]
    zenith = 1

    if j: z,c = c,z 

    if c == complex(0,0) and pwr < 0: return z,i

    if pwr < 0: z += [c]

    while (abs(zenith) < limit) and i != itr :

        i += 1

        z += [z[-1] ** pwr + c]
        zenith = z[-1]

    return z #Return coordinate vector of all zs


#items under this line need to be updated to the new output format

def sakura(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Sakura Set ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    p = z

    while abs(z) < limit and i != itr:

        i += 1

        zl = z

        z = (z*p*c) ** pwr + c

        p = zl

    return z,i

def mBar(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Mandelbar Set ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    while abs(z) < limit and i != itr:

        i += 1

        z = z.conjugate() ** pwr + c

    return z,i


def bShip(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Burning Ship ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    while abs(z) < limit and i != itr:

        i += 1

        z = (abs(z.real)+abs(z.imag)*j) ** pwr + c

    return z,i


def bSaku(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Burning Sakura ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    p = z

    while abs(z) < limit and i != itr:

        i += 1

        zl = z

        z = (complex(abs(z.real),abs(z.imag))
             *complex(abs(c.real),abs(c.imag))
             *complex(abs(p.real),abs(p.imag))) ** pwr + c

        p = zl

    return z,i

def sinBrot(z,c,pwr,itr,limit,j = False,i = 0):

    '''Sinebrot ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    limit *= 3 # Necessary for good detail due to sin.

    while abs(z) < limit and i != itr:

        i += 1

        z = cmath.sin(z) ** pwr + c

    return z,i

def duck(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Burning Ship ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    while abs(z) < limit and i != itr:

        i += 1

        z = complex(z.real,abs(z.imag)) ** pwr + c

    return z,i

class Formula(object):

    z = 0
    c = 0
    pwr = 0
    itr = 0
    limit = 0
    j = False
    ex = False
    i = 0

def kel(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Burning Ship ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    while abs(z) < limit and i != itr:

        if i%2== 0: z = z ** pwr + c
        else:

            if i % 3 == 0: z = z ** pwr / c
            else: z = z ** pwr - c


        i += 1

    return z,i


def apollyon(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Fractal with apollonian julia-packing.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    while abs(z) < limit and i != itr:

        z = (c/z) - z ** pwr + c
        
        i += 1

    return z,i

def superset(z,c,pwr,itr,limit, j = False,ex = False, i = 0):

    output = calculate(fSet,pwr,itr,False if julia else True,0,0,True,10,10)

    for vals in range(len(output)):
        rgb[vals%3] += output[vals]

    return [int(rgb[i]/(len(output)/3)) for i in range(len(rgb))]
    

eqs = [mandelbrot,sakura,mBar,bShip,bSaku,sinBrot,duck,apollyon,kel]



from random import random
def estimate():
    a = 0
    b = 0
    c = []
    while True:
        a +=1 if len(mandelbrot(0,complex(random()*3 - 2,random()*2.5 - 1.25),2,80,4)) is 81 else 0
        b+=1
        if b%1000000 == 0:
            c += [a/b * 3*2.5]
            a = 0
            b = 0
            if len(c) % 5 == 0:
                print(sum(c)/len(c))

    return a/b
