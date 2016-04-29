#colouring.py
#Colouring algorithms for Fractale

import math
import cmath
from cspace import CSpace

class Colouring(object):

    '''Class for colouring escape-time fractals.'''

    '''Due to load order, this stuff has to go first.'''

    #Tools
    def interpolate(self,n):

        #Determine what the colour would be if n was one of the integers it
        #sits between.
        floor = self.pallet[int(n)%len(self.pallet)]
        ceiling = self.pallet[(int(n)+1)%len(self.pallet)]

        #N can be negative. Bytes cant.
        absn = abs(n)

        #Determine distance of decimal part of n from ceiling and floor.
        cDist = absn - int(absn)
        fDist = 1-cDist

        #Return a colour that far from the two primaries.
        return [abs(int(cDist*ceiling[i] + fDist*floor[i])) for i in range(3)]

    def rotate(self,n):

        '''Rotate the pallet.
           n = any non-negative number.
           TODO: Fractional rots. W/Interpolation, should allow the simulation
           through not reality of the Fractional Iteration Method. 
        '''


        self.pallet = self.pallet[rot%len(pals[indice]):] +\
                 self.pallet[:rot%len(pals[indice])]

        

    #Colouring Algorithms

    ###Interior+Exterior
    def mono(self,z,escTime,itr,c):

        ext = [0,0,0]
        inte = [255,255,255]

        if escTime == itr:
            return ext

        return ext

    def negarc(self,z,escTime,itr,c):

        return self.interpolate(z.real - abs(z.imag))

        #return self.pallet[int(z.real - abs(z.imag))%len(self.pallet)]

    ###Exterior-only
    def eta(self,z,escTime,itr,c):

        return self.pallet[escTime%(len(self.pallet))]

    def etaSm(self, z, escTime, itr,c):

        
        escTime = abs(escTime + 1 - (cmath.log( cmath.log(abs(z)) /
                                            cmath.log(2) ) / cmath.log(2)))
        

        return self.interpolate(escTime.real)

    #Experimental

    def arcinv(self, z, escTime, itr, c):
    
        r = abs(z.real)
        g = abs(z.imag)
        b = abs(z)

        rgb = [i/(r+g+b) for i in [r,g,b]]
#int(255*(2- n)/2)%256
        self.CSpace.setRGB(rgb)
        self.CSpace.rgb2hsv()
        self.CSpace.hsv[2] = sum(rgb)-self.CSpace.hsv[2]

        return [int(255*(2-i)/2)%256 for i in self.CSpace.hsv2rgb()]

    def expy(self, z, escTime, itr, c):

        c = (z/abs(z))*.65
        z = 0
        zenith = 1
        i=0

        while (abs(zenith) < 4) and i != 44:

            i += 1

            z = z ** 2 + c
            zenith = z

        

        return self.etaSm(z,i,0,0)

    '''This is where the init and seedvars are.''' 
    #Algorithm Control Vars
    pal = 0
    inside = 0
    outside = 0

    #Int/Ext Algorithms
    iCAs = [mono,negarc]
    oCAs = [eta,negarc,mono]

    #Basic Pallets
    pale = [
        #Basic Rainbow
        [[255, 0, 0],[255, 69, 0],[255, 255, 0],
        [0, 255, 0],[0, 128, 128],[0, 0, 255],
        [128, 0, 128],[255, 0, 255]],
        #Green-Blue-Red slide.
        [[127, 127, 0], [63, 191, 0], [0, 255, 0],
         [0, 191, 63], [0, 127, 127], [0, 63, 191],
         [0, 0, 255], [63, 0, 191], [127, 0, 127],
         [191, 0, 63], [255, 0, 0], [191, 63, 0]],
        #Classic Blue-Black-Amber-White
        [[25,7,26],[9,1,47],[4,4,73],[0,7,100],
         [12,44,138],[24,82,177],[57,125,209],
         [134,181,229],[211,236,248],[241,233,191],
         [248,201,95],[255,170,0],[204,128,0],
         [157,87,0],[106,52,3],[66,30,15]],
        #Smooth Rainbow
        [[255, 0, 0], [255, 63, 0], [255, 127, 0], [255, 191, 0],
         [255, 255, 0], [191, 255, 0], [127, 255, 0], [63, 255, 0],
         [0, 255, 0], [0, 255, 63], [0, 255, 127], [0, 255, 191],
         [0, 255, 255], [0, 191, 255], [0, 127, 255], [0, 63, 255],
         [0, 0, 255], [63, 0, 255], [127, 0, 255], [191, 0, 255],
         [255, 0, 255], [255, 0, 191], [255, 0, 127], [255, 0, 63]],
        #Less Smooth Rainbow
        [[255, 0, 0], [255, 127, 0],
         [255, 255, 0], [127, 255, 0],
         [0, 255, 0], [0, 255, 127],
         [0, 255, 255], [0, 127, 255],
         [0, 0, 255], [127, 0, 255],
         [255, 0, 255], [255, 0, 127]]
        ]
    
    def __init__(self):

        self.pallet = self.pale[self.pal]
        self.insideC = self.iCAs[self.inside]
        self.outsideC = self.oCAs[self.outside]
        self.CSpace = CSpace()

    def updateInside(self,inside):

        self.inside = inside

    def updateMulti(self,**kargs):

        for i in kargs: setattr(self,i,kargs[i])

        self.__init__()
        

    #CA Switches.
##    def setoutsideC(self):
##
##        if algorithm == 0: #Low kolgomorov scheme; border analysis
##            return self.mono
##
##        elif algorithm == 1: #Escape-Time
##
##            return self.eta
##
##        elif algorithm == 2: #ET + Comps of Z
##            
##            return pal[int(z.real+z.imag+escTime)%len(pal)]
##
##        elif algorithm == 3: #Seems to operate a bit like NIC?
##
##            return pal[int((abs(z)+escTime)*2)%len(pal)]
##
##        elif algorithm == 4: #Truth tables, maybe?
##
##            return pal[((int(z.real) ^ int(abs(z.imag)))//escTime)%len(pal)]
##
##        elif algorithm == 92271: #Experimental
##
##            return pal[int(z.real - abs(z.imag))%len(pal)]
##
##            #Ringlike Structures. Seems to show "boundaries".
##            #pal[int(abs(z)*1000)%len(pal)]
##
##        
##
##
##def colour(algorithm,z,escTime,itr):
##
##    
##
##    if escTime < itr:
##        #Exterior Colouring
##        
##        if algorithm == 0: #Low kolgomorov scheme; border analysis
##            return [255,255,255]
##        
##        elif algorithm == 1: #Escape-Time
##
##            return pal[escTime%(len(pal))]
##
##        elif algorithm == 2: #ET + Comps of Z
##            
##            return pal[int(z.real+z.imag+escTime)%len(pal)]
##
##        elif algorithm == 3: #Seems to operate a bit like NIC?
##
##            return pal[int((abs(z)+escTime)*2)%len(pal)]
##
##        elif algorithm == 4: #Truth tables, maybe?
##
##            return pal[((int(z.real) ^ int(abs(z.imag)))//escTime)%len(pal)]
##
##        elif algorithm == 92271: #Experimental
##
##            return pal[int(z.real - abs(z.imag))%len(pal)]
##
##            #Ringlike Structures. Seems to show "boundaries".
##            #pal[int(abs(z)*1000)%len(pal)]
##        
##                
##    else:
##        #Interior Colouring
##        return [0,0,0]
##
##
##
###Pallets
##
##def pale(indice,rot=0):
##
##    '''Output a pallet. Optionally allows rotation.
##       Rotation DOES NOT take negatives.'''
##
##
##    output = pals[indice][rot%len(pals[indice]):] +\
##             pals[indice][:rot%len(pals[indice])]
##    
##    return output
##
##pal = pale(2)
