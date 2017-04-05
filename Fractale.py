##Custom Classes
from graph import Graph
from colouring import Colouring
from output import PPX
import random

#Custom Functions
from cTools import toPPX,tBaseN,e
#from mathtricks import *
from eqs import *

#Builtin Functions
from random import randint

#Whole libs
import cmath

#Initialize Objects

plane = Graph()
field = Graph()
colour = Colouring()


#### Begin Program Proper ###

#Set things up so the program can output a bitmap for
#arbitrary params and then display it.

#At the moment, the suprset algo is naieve
#This inhibits proper visualisation of structure
#Prop fix: Scalar Supersets.
#Nessec: Need to determine a point field to take samples from
#corres to graph. Some avg of points.




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


#Main calculation function
#Run the colouring algo before using symmetry. Fucking seriously. It's faster.

def calculate(fSet,pwr,itr,julia,zBase,cBase,opt,resX,resY,n,transform,raw):

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
    output = [] #Stores raw output; basically for Supersets only.
    curLine = [] #Stores colour output; for image writing
    

    #Set up the graph for rendering.
    plane.updateRes(resX,resY)
    plane.updateMulti(epicentre=[-.75,0],magnitude=0)

    #Set up colouring algorithm for colouring.
    colour.updateMulti(pal=3)
    cinter = colour.cPic(5)
    couter = colour.cPic(4)

    #Set up output container.
    out = PPX()
    out.setMost(3,1,resX,resY,'Output'+str(n))

    #Assign function to be called
    fSet = eqs[fSet]

    #Iterate over the space.
    for y in range(resY):


        for x in range(resX):

            c = complex(plane.posX, plane.posY) + cBase
            z = zBase

            z = fSet(z,c,pwr,itr,limit,julia,transform)

            escTime = len(z)-1

            if not raw:
                if escTime == itr:
                    curLine += cinter(z,escTime,itr,c)
                else: curLine += couter(z,escTime,itr,c)

            plane.posX += plane.fsX

        plane.posX = plane.reset[0]
        plane.posY += plane.fsY

        if not raw:
            out.write(curLine)
            curLine = []
        else: output += [[z[-1],len(z)-1]]

##        if opt and plane.posY > 0:
##            #best case div rendertime/2
##            output += symmetry(output,julia,y,resY,resX)
##            break
        
    if raw: return output
    else: return -1

#Rendering Modes

def run(x,y, fSet):

    calculate(fSet,2,80,0,(0j),(0+0j),False,x,y," Raw ",lambda c:c,True)
    print("Render Complete.")

def superset(j,x,y,itr,sSym=False):

    '''Superset Fractal Calculator. /Expensive./
    j = size of julia sets to be calculated.
    x,y = final size of image
    itr = number of iterations to run for.
    sSym = if fractal is symmetrical beneath 0i, setting this to true cuts the
    ----rendering time in half. Note, if fractal is assymetrical, will cause
    ----innacurate results. If fractal has rotal symetry in a power of 2, set to
    ----2. Due to fundamental limitations in the current implementation,
    ----odd-n rotal symmetry cannot be rendered properly.
    '''

    field.updateMulti(resX=x,resY=y,magnitude=1)
    
    #Julia Coords for inverse supersets.   
    cX,cY = 0,0#-.783091,-.149219#.296906,.502234

    final = []

    formSet = 1
    mSet = True
    curLine = []
    out = PPX()
    out.setMost(3,1,x,y,'SuperOutput')
    colour.updateMulti(pal=3)
    cAlg = colour.cPic(1)

    for rows in range(y):

        for points in range(x):

            z =  calculate(formSet,2,itr,mSet,complex(field.posX,field.posY)
                               ,complex(cX,cY),0,j,j,"",lambda c: c,True)

            javg = sum([i[0] for i in z])/j**2
            escAvg = sum([i[1] for i in z])/j**2

            curLine += cAlg(0,escAvg,0,0)

            field.posX += field.fsX

        
        
        #Satisfy idle curiosity
        if rows%15 == 1: print('Render is',str(round((rows/y)*(2 if sSym else 1)
                                                     *100, 3))+'% done.')
        out.write(curLine)
        field.posY += field.fsY
        field.posX = field.reset[0]

        curLine = []

        

    print("Render complete.")

    #toPPX(3,True,final,x,y,fname='Renders/c('+str(cX)+','+str(cY)+') at '+str(j)
     #     +' ['+tBaseN(randint(0,1230942345))+']')

run(100,100,0)
superset(10,100,100,0)
