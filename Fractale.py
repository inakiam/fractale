#Custom Classes
from graph import Graph
from colouring import Colouring
import random

#Custom Functions
from cTools import toPPX,tBaseN,e
from mathtricks import *

#Builtin Functions
from random import randint

#Whole libs
import cmath    

#### Begin Program Proper ###

#Set things up so the program can output a bitmap for
#arbitrary params and then display it.

#Also, project after classification and variable
#generalisation is  the following
#Render point
#Render next one row down
#Repeat pattern, gng two rows down
#use transitive comparison to implement
#SG-like algorithm.

#At the moment, the suprset algo is naieve
#THis inhibits proper visualisation of structure
#Prop fix: Scalar Supersets.
#Nessec: Need to determine a point field to take samples from
#corres to graph. Some avg of points.


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

def sinebrot(z,c,pwr,itr,limit,j = False,i = 0):

    '''Sinebrot ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    limit *= 3 # Necessary for good detail due to sin.

    while abs(z) < limit and i != itr:

        i += 1

        z = cmath.sin(z) ** pwr + c

    return z,i

def mandelduck(z,c,pwr,itr,limit,j = False,ex = False,i=0):

    '''Burning Ship ETA.'''

    if j: z,c = c,z #Invert coordinate pairs for Julia

    while abs(z) < limit and i != itr:

        i += 1

        z = complex(z.real,abs(z.imag)) ** pwr + c

    return z,i

def keloggbrot(z,c,pwr,itr,limit,j = False,ex = False,i=0):

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




#Switch Function: Assign a Render Function to Invariant Code
def ePic(n):

    '''Equation Selection Function.'''

    if n == 0: function = mandelbrot
    elif n == 1: function = sakura 
    elif n == 2: function = mBar
    elif n == 3: function = bShip
    elif n == 4: function = bSaku
    elif n == 5: function = sinebrot
    elif n == 6: function = mandelduck
    elif n == 7: function = keloggbrot
    elif n == 8: function = apollyon

    return function

def cPic(obj,n):

    if n==0: function = obj.mono
    elif n==1: function = obj.eta
    elif n==2: function = obj.negarc
    elif n==3: function = obj.etaSm
    elif n == 4: function = obj.arcinv
    elif n==92271: function = obj.expy

    return function

#Symmetry Optimization

def symmetry(rawIn,julia,yNow,yFinal,x):

    '''Return a rotated or mirrored version of input.'''

    output = []

    yNow += 1

    if julia:
        
        #Julias that are symmetrical show rotal symmetry,
        #so they need a different algorithm

        for i in range(-1,(-x*3*(yFinal-yNow)),-3):
            output += [rawIn[i-2],rawIn[i-1],rawIn[i]]
        

    else:

        #copy rawIn, in order, to an array, packing it by line
        #then use extended list slicing to invert the order.
        intermediate = [[rawIn[nums+rows] for nums in range(x*3)]
                  for rows in range(0,(x*3*(yFinal-yNow)),x*3)][::-1]

        for i in range(len(intermediate)):
            output += intermediate[i]

       

    return output


#Objects. Let's not initialize objects every fucking function.
plane = Graph()
field = Graph()
colour = Colouring()

#Main calculation function
#Run the colouring algo before using symmetry. Fucking seriously. It's faster.

def calculate(fSet,pwr,itr,julia,zBase,cBase,opt,resX,resY):

    '''ETA Fractal Calculator.
    fSet defines formulas; see function ePic for details.
    pwr defines the exponet of the formula
    itr defines number of iterations
    julia defines if the formula should be run in Julia mode.
    zBase defines the Julia seed/Mset perturbation.
    opt switches on different optimization modes
    ---opt should be an even n if the fractal is
    ---assymetrical on the real axis (bShip, bSaku)
    resX and Y set the resolution of the output image'''

    limit = 4 #How high the absolute value of Z must be to escape the set.

    #Output Variables
    rawOut = []
    output = []

    #Set up the graph for rendering.
    plane.updateRes(resX,resY)
    plane.updateMulti(epicentre=[0.5,0],magnitude=3)

    #Set up colouring algorithm for colouring.
    colour.updateMulti(pal=3)
    cinter = cPic(colour,4)
    couter = cPic(colour,3)

    #Assign function to be called
    renderMethod = ePic(fSet)

    soi = (3)

    #Iterate over the Graph.
    for y in range(resY):


        for x in range(resX):

            c = complex(plane.posX, cmath.sqrt(plane.posY)) + cBase
            z = zBase

            z = renderMethod(z,c
                             ,pwr,itr,limit,julia)

            z,escTime = z[-1],len(z)-1

            if escTime == itr:
                output += cinter(z,escTime,itr,c)
            else: output += couter(z,escTime,itr,c)

            plane.posX += plane.fsX

        plane.posX = plane.reset[0]
        plane.posY += plane.fsY

        if opt and plane.posY > 0:
            #If the fractal is symmetrical, copy output across plane of symmetry
            output += symmetry(output,julia,y,resY,resX)
            break

    return output

#Rendering Algorithms

def run(x,y, fSet):

    output = calculate(fSet,2,80,0,(0j),(0+0j),True,x,y)
    print("Render Complete. Writing to file...")
    toPPX(3,True,output,x,y,fname = 'Renders/render')
    print("Done.")

def superset(j,x,y,itr,sSym=False):

    '''Superset Fractal Calculator. /Expensive./
    jX = size of julia set X, jY same for y
    x,y = final size of image
    itr = number of iterations to run for.
    sSym = if fractal is symmetrical beneath 0i, setting this to true cuts the
    ----rendering time in half. Note, if fractal is assymetrical, will cause
    ----innacurate results. If fractal has rotal symetry in a power of 2, set to
    ----2. Due to fundamental limitations, odd-n rotal symmetry cannot be
    ----rendered with supersymmetry.
    '''

    field.updateMulti(resX=x,resY=y,magnitude=1)
    
    #Julia Coords for inverse supersets.   
    cX,cY = 0,0#-.783091,-.149219#.296906,.502234
    #reset = zX

    final = []

    formSet = 1
    mSet = True

    for rows in range(y):

        for points in range(x):

            output = calculate(formSet,2,itr,mSet,complex(plane.posX,plane.posY)
                               ,complex(cX,cY),0,j,j)
            rgb = [0,0,0]

            field.posX += field.fundamentalStep

            #Accumulate the pixels in output into a single-pixel list
            for vals in range(len(output)):
                rgb[vals%3] += output[vals]

            #rgb = [output[i%3] for i in output]

            #Add to final a pixel which is the average of all pixels in output
            final += [int(rgb[i]/(len(output)/3)) for i in range(len(rgb))]

        #Print progress every fifty rows so the user knows that the program has
        #not halted.
        if rows%15 == 1: print('Render is',str(round((rows/y)*(2 if sSym else 1)
                                                     *100, 3))+'% done.')

        field.posY += field.fundamentalStep
        field.posX = field.reset[0]

        if sSym and field.posY > 0:
            final += symmetry(final,0,rows,y,x)
            break #symmetry breaks XD

    print("Render complete.")

    toPPX(3,True,final,x,y,fname='Renders/c('+str(cX)+','+str(cY)+') at '+str(j)
          +' ['+tBaseN(randint(0,1230942345))+']')

def rmacro(x,y):

    '''Macro for rSuper tht poduces a Relational Superset of *all* julia points
       for a mandelbrot of the resolution given. Also works for other fractals
       with a line of symmetry at x=0.
    '''

    plane.updateRes()
    

def rSuper(coordinates,j,x,y,itr,sSym=False):

    '''Relational Superset Fractal Calculator.
       Creates supersets of a given list of points.
    '''

    field.updateMulti(resX=x,resY=y,
                      epicentre=[.935,.725]#[-.76783964756993821433,-.11716982989737652794]
                      ,magnitude=1)
    
    #Julia Coords for inverse supersets.   
    cX,cY = 0,0#-.783091,-.149219#.296906,.502234
    #reset = zX

    final = []

    formSet = 0
    mSet = True

    for rows in range(y):

        for points in range(x):

            for locations in coordinates:
                pass

            output = mandelbrot()
            rgb = [0,0,0]

            field.posX += field.fundamentalStep

            #Accumulate the pixels in output into a single-pixel list
            for vals in range(len(output)):
                rgb[vals%3] += output[vals]

            #rgb = [output[i%3] for i in output]

            #Add to final a pixel which is the average of all pixels in output
            final += [int(rgb[i]/(len(output)/3)) for i in range(len(rgb))]

        #Print progress every fifty rows so the user knows that the program has
        #not halted. For weak minds.
        #if rows%15 == 1: print('Render is',str(round((rows/y)*(2 if sSym else 1)
                                                     #*100, 3))+'% done.')

        field.posY += field.fundamentalStep
        field.posX = field.reset[0]

        if sSym and field.posY > 0:
            final += symmetry(final,0,rows,y,x)
            break #symmetry breaks XD

    print("Render complete.")

    toPPX(3,True,final,x,y,fname='Renders/c('+str(cX)+','+str(cY)+') at '+str(j)
          +' ['+tBaseN(randint(0,1230942345))+']')

man ='''Fractale: A Fractal Fractal Render Renderer

USAGE: Fractale is a fractal renderer that specialises in producing so-called
superset renders. These renders are achieved via rendering the given fractal's
Julia (Julias for mandelbrot-like fractals, perturbed mandelbrot-likes for
julias.)

Fractale has two use modes. In the first, the program is run without any
command line parametres. This boots the program into a mode that allows the user
to enter in parametres through a series of simple prompts. This mode is self
explanitory, so documentation will end at noting its existence.

In the second mode, Fractale is run via command line parametres.

AVAILIBLE PARAMETRES:

    -h, --help: Display this guide. Priority 1, all other inputs ignored.

    -sSet: Display a brief description of the superset algorithm. Priority 2,
           all other inputs ignored.

    -about: Display an ode to the coder's ego. Priority infinity, always
            ignored.

    -r: Rendering mode. 0 is superset, and is default. 1 is normal set.

    -f: Base formula. 0 is default.
       -0: Mandelbrot
       -1: Sakura
       -2: Mandelbar
       -3: Burning Ship
       -4: Burning Sakura

    -p: The exponent of the formula. Larger = slower rendering. Default of 2.

    -j: Julia mode. If 1, will render a julia set. Default 0.
        NOTE: setting j = 1 swaps the position of c and z.

    -e: Where the centre of the picture is on the coordinate plane.
        Default of 0,0.

    -m: How much the picture is zoomed. Default 1. Doubling doubles zoom.

    -z: variable z's starting value; default 0,0.

    -c: variable c's startying value; default 0,0.

    -xy: Final image's resolution.

    -jxy: Subset resolution for superset rendering. This is by far the largest
          performance bottleneck in the program.

    -oa: Colouring algorithm. 0 is default.
       -0: Escape Time
       -1: Not yet implemented.

    -ia: Interior CA. Not yet implemented

    -pal: Pallet. 0 is default; customs can be loaded or passed directly.
        -0: Basic Rainbow
        -1: G-B-R Slide
        -2: Classic blue-amber-white-black
        -$PATH: Path to a text file containing a custom pallet(s).
                -If multiple, give index as (n).
        -Direct: To pass a pallet diectly, use the following format.
         -[[R,G,B],[R,G,B],...] Make the last colour what you want the
         -interior of the set to be coloured as (if not using -ia).

CREDITS:

    NO ONE AND NOTHING. I kid. Benoit Mandelbrot for if you don't know the
    significance of this man, who are you and why are you using this program,
    Michael Michelitsch and Otto E. Rössler for the Burning Ship formula,
    Eric Baird (?) for the Mandelbar formula (I'm going off a single webpage
    of unknown credibility here, if I'm wrong, tell me please!), 
    (NAMES, formulas)

    To the best of my knowledge, the Sakura Set is my own derivation; as do we
    all, I stood on the shoulders of giants. Burning Sakura was inspired by the
    obvious.

LICENCE:

    CC-BY-NC 3.0. Extensible to derivatives; if you seriously want to try selling
    stuff you make with this - send me some negligible amount of crypto with a
    transaction comment including the name you intend to sell under - trade names
    are fine - and the site you intend to do so on, if extant.

    In return, the licnse on your copy becomes CC-BY 3.0.

    Seriously though, don't send me more than a few pennies, this is just a
    way for me to be able to see the cool things you people are doing without
    giving out an email.

    BTC:
    LTC:
    DOGE:
    -suggest any new and interesting currencies.

'''
sSetExp = '''Superset Rendering: Quick Description

Superset rendering works on the essential concept

'''

about = "Egode. Seriously?"
