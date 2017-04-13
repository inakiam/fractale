#Factal Eqs


def mandelbrot(z,c,pwr,itr,limit,j,transform):

    '''Mandelbrot/Julia ETA.'''
    if j: z,c = c,z
    z = [z]
    zenith = 1
    i=0

    try:
        c = transform(c)
    except ZeroDivisionError:
        return z # Not like it was going anywhere...

    #LETS NOT DIVIDE BY ZERO
    if c == complex(0,0) and pwr < 0: return z

    if pwr < 0: z += [c]

    while (abs(zenith) < limit) and i != itr :

        i += 1

        z += [z[-1] ** pwr + c]
        zenith = z[-1]
        if len(z) > 5:
            pass

    return z #Return coordinate vector of all zs

#saku preloop
p = z
#saku loop
zl = z
z = (z*p*c) ** pwr + c
p = zl



#mBar
z = z.conjugate() ** pwr + c

#bShipppppp
z = (abs(z.real)+abs(z.imag)*j) ** pwr + c


#bSaku preloop
p = z
#bSaku Loop
zl = z

z = (complex(abs(z.real),abs(z.imag))
     *complex(abs(c.real),abs(c.imag))
     *complex(abs(p.real),abs(p.imag))) ** pwr + c

p = zl




#sinBrot. limit should be multiplied by 3 for better deets
z = cmath.sin(z) ** pwr + c




#duck
z = complex(z.real,abs(z.imag)) ** pwr + c



#kel
if i%2== 0: z = z ** pwr + c
else:

    if i % 3 == 0: z = z ** pwr / c
    else: z = z ** pwr - c




#apollyon
z = (c/z) - z ** pwr + c



    

eqs = [mandelbrot,sakura,mBar,bShip,bSaku,sinBrot,duck,apollyon,kel]