#Factal Eqs


def mandelbrot(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Mandelbrot/Julia ETA.'''

    z=[z]
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

eqs = [mandelbrot,sakura,mBar,bShip,bSaku,sinBrot,duck,apollyon,kel]
