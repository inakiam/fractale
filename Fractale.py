##Custom Classes
from colouring import Colouring
from graph import Graph
from output import PPX
# Custom Functions
from eqs import *


# Builtin Functions

# Whole libs

# Initialize Objects

plane = Graph()
field = Graph()
colour = Colouring()


#### Begin Program Proper ###

# Set things up so the program can output a bitmap for
# arbitrary params and then display it.

''' At the moment, the suprset algo is naive. The structure visualised is beautiful, and coherent, but also essentially
wholly arbitrary. What needs to be done, once I make this the class it always should have been is to add a rendering
mode for supersets such that a superset can be rendered using points that bear various well-defined relations.
Instead of sampling the julia along the interval [-2-2i,2+2i], or whatever, once might use roots of the original point,
logarithms. Or what-have-you.'''

# Main calculation function
# Run the colouring algo before using symmetry. Fucking seriously. It's faster.

def calculate(fSet, pwr, itr, julia, zBase, cBase, opt, resX, resY, n, transform, raw):
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

    limit = 4  # How high the absolute value of Z must be to escape the set.

    # Output Variables
    output = []  # Stores raw output; basically for Supersets only.
    curLine = []  # Stores colour output; for image writing

    # Set up the graph for rendering.
    plane.updateRes(resX, resY)
    plane.updateMulti(epicentre=[0, 0], magnitude=1)

    # Set up colouring algorithm for colouring.
    colour.updateMulti(pal=3)
    cinter = colour.cPic(5)
    couter = colour.cPic(4)

    # Set up output container.
    if not raw:
        out = PPX()
        out.setMost(3, 1, resX, resY, 'Output' + str(n))

    # Assign function to be called
    fSet = eqs[fSet]

    # Iterate over the space.
    for y in range(resY):

        for x in range(resX):

            c = complex(plane.posX, plane.posY) + cBase
            z = zBase

            z = fSet(z, c, pwr, itr, limit, julia, transform)

            escTime = len(z) - 1

            if not raw:
                if escTime == itr:
                    curLine += cinter(z, escTime, itr, c)
                else:
                    curLine += couter(z, escTime, itr, c)
            else:
                output += [[z[-1], len(z) - 1]]

            plane.posX += plane.fsX

        plane.posX = plane.reset[0]
        plane.posY += plane.fsY

        if not raw:
            out.write(curLine)
            curLine = []


        ##        if opt and plane.posY > 0:
        ##            #best case div rendertime/2
        ##            output += symmetry(output,julia,y,resY,resX)
        ##            break

    if raw:
        return output
    else:
        return -1


# Rendering Modes

def run(x, y, fSet, j):
    calculate(fSet, 2, 80, j, (.1 + .2j), (0 + 0j), False, x, y, " Raw ", lambda c: c, False)
    print("Render Complete.")


def superset(j, x, y, itr, sSym=False):
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

    field.updateMulti(resX=x, resY=y, epicentre=[-.75, 0], magnitude=-.2)

    # Julia Coords for inverse supersets.
    cX, cY = 0, 0  # -.783091,-.149219#.296906,.502234

    final = []

    color = Colouring()
    formSet = 0
    mSet = True
    curLine = []
    outp = PPX()
    outp.setMost(3, 1, x, y, 'SuperOutput')
    color.updateMulti(pal=2)
    cIn = color.cPic(1)
    cOu = [0, 0, 0]

    for rows in range(y):

        for points in range(x):
            z = calculate(formSet, 2, itr, mSet, complex(field.posX, field.posY)
                          , complex(cX, cY), False, j, j, "", lambda c: c, True)

            javg = sum([i[0] for i in z]) / j ** 2
            escAvg = sum([i[1] for i in z]) / j ** 2

            curLine += [round(i - escAvg / itr * i) for i in cIn(0, escAvg, 0, 0)]

            field.posX += field.fsX

        # Satisfy idle curiosity
        if rows % 15 == 1: print('Render is', str(round((rows / y) * (2 if sSym else 1)
                                                        * 100, 3)) + '% done.')
        outp.write(curLine)
        field.posY += field.fsY
        field.posX = field.reset[0]

        curLine = []

    print("Render complete.")


class Fractale(object):

    #The recursion
    if base: supercalc = Fractale(base = False)

    #Objects of Use
    colour = Colouring
    plane = Graph()
    if base: out = PPX()

    #Polymorphic Storage Vars; because I'm lazy.
    eqs =


    #Default values
    ##Mandel/Julia Switch
    baseSetMandel = True
    superSetJulia = not(baseSetMandel)
    ##Iteration Depth
    itr = 80
    ##Bailout Value: Stop calculation when abs(z) exceeds.
    limit = 4
    ##Base values of z,c
    zBase = 0j
    cBase = 0j
    ##Fractal set id
    fSet = 0
    ##Image Resolution
    resX = 100
    resY = 100

    def __init__(self,base=True):


    def setAlgo(self,algo):
        algId = ["Normal","Linear Superset","Radrec Superset"].find(algo)

        self.algo = self.algorithms[algId]

    def setZPerturbation(self, real, imag):
        self.zBase = complex(real, imag)

    def setbaseSetMandel(self, switch):
        self.baseSetMandel = switch
        self.superSetJulia = not(self.baseSetMandel)
        #if false, is julia



#run(100,100,0,True)
#superset(10, 100, 100, 40)
