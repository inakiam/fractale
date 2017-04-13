from cmath import *
##Custom Classes
from colouring import Colouring
from graph import Graph
from output import PPX
# Custom Functions
from eqs import *
from cTools import *


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
    output = [[],[]]  # Stores raw output; basically for Supersets only. [[points in set],[points outside]]
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
                if escTime == itr:
                    output[0] += [[z[-1], escTime]]
                else:
                    output[1] += [[z[-1],escTime]]

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

    field.updateMulti(resX=x, resY=y, epicentre=[-.75, 0], magnitude=0)

    # Julia Coords for inverse supersets.
    cX, cY = 0, 0  # -.783091,-.149219#.296906,.502234

    final = []

    color = Colouring()
    formSet = 0
    mSet = True
    curLine = []
    outp = PPX()
    outp.setMost(3, 1, x, y, 'SupeeeqwerOutput')
    color.updateMulti(pal=0)
    cOut = color.cPic(1)
    cIn = [0, 0, 0]

    for rows in range(y):

        for points in range(x):
            zIn,zOut = calculate(formSet, 2, itr, mSet, complex(field.posX, field.posY)
                          , complex(cX, cY), False, j, j, "", lambda c: c, True)


            escAvg = sum([i[1] for i in zOut]) / j ** 2
            

            curLine += cOut(0, escAvg, 0, 0)

            field.posX += field.fsX

        # Satisfy idle curiosity
        if rows % 15 == 1: print('Render is', str(round((rows / y) * (2 if sSym else 1)
                                                        * 100, 3)) + '% done.')
        outp.write(curLine)
        field.posY += field.fsY
        field.posX = field.reset[0]

        curLine = []

    print("Render complete.")

class Fractale(Graph,Colouring):



''' NEW DEV TARGET: Since the renderer can give all julias intact; make a progream for outputting julia mosaics. '''
'''DISTANCE COLOUR ALGO. SET Z = FURTHEST POINT FROM CENTRE TO BE RENDERED. LET ANY POINT ABS(Z) BE 50% GREY.
THEN INFINITY IS WHITE, AND ZERO IS BLACK. MAybe acomplishable with a fraction with preset numerator??? Set numer = a(z)
let denom be a(z), but raise a(z) to negative power st @ infinity, div by 0, at 0, div by infinity.
'''
    #Objects of Use
    Colouring().__init__()

    #Polymorphic Storage Vars; because I'm lazy.
    eqs = 1


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

    ##Point Generation Algorithm
    algo = 0
    ##Rendering Method.
    rMode = min(algo,1)

    #Variables to be passed down to recursive instance
    pointCloud = None

    def __init__(self,base=True,antecedent = None):

        #Setup Graph...
        Graph.__init__()
        Graph.(resX=self.resX, resY=self.resY, epicentre=[-.75, 0], magnitude=0)


        #Inconstants
        if base:
            #create things not necessary in recursive calculators
            self.superCalc = Fractale(base = False,self)
            self.out = PPX()
            self.out.setMost(3,1,resX,resY,'Fractale [' +str(tBaseN(randint(1,4000))) + ']')
        else:
            #Give supercalc access to Parent
            self.Parent = antecedent

            #autoconfigure sSet render with some defaults...
            self.algo = self.Parent.algo
            self.rMode = min(rMode, 1)
            self.resX = 10
            self.resY = 10


            #Make vars not needed in Base instance.
            self.output = [[],[]] #[inside set],[out]

    def __genCloud__(self,c):
        '''Generates a number of roots ~= julia pixelres.'''

        out = []

        triangle = round(.5 * (1 + (8 * (self.resX * self.resY) + 1) ** .5))

        for i in range(1, triangle + 1):
            out += allComplexRoots(c, i)

        return out




    def setAlgo(self,algo):
        algId = ["Normal","Linear Superset","Radrec Superset"].find(algo)

        self.algo = self.algorithms[algId]

    def setZPerturbation(self, real, imag):
        self.zBase = complex(real, imag)

    def setImageCentre(self,real, imag):
        Graph.updateEp(epicentre = [real,imag])

    def setZoom(self,zoom):
        Graph.updateMag(zoom)

    def setbaseSetMandel(self, switch):
        self.baseSetMandel = switch
        self.superSetJulia = not(self.baseSetMandel)
        #if false, is julia

    def render(self):

        #raw output var
        rOut = []

        if self.rMode == 0:

            for y in range(resY):

                for x in range(resX):

                    c = complex(Graph.posX, Graph.posY) + cBase
                    z = zBase

                    z = fSet(z, c, pwr, itr, limit, julia, transform)

                    escTime = len(z) - 1

                    if not raw:
                        if escTime == itr:
                            curLine += cinter(z, escTime, itr, c)
                        else:
                            curLine += couter(z, escTime, itr, c)
                    else:
                        if escTime == itr:
                            output[0] += [[z[-1], escTime]]
                        else:
                            output[1] += [[z[-1], escTime]]

                    Graph.posX += Graph.fsX

                Graph.posX = Graph.reset[0]
                Graph.posY += Graph.fsY

                if self.algo == 0:
                    out.write(curLine)
                    curLine = []
            #Return Values for graph renders...
            if self.algo == 1:
                return rOut
            elif:
                return -1

        elif self.rMode == 1 and not(self.Base): # this rendermode makes no sense for base sets

            pointCloud = self.__genCloud__(self.c)

            for c in pointCloud:

                eqs.escTime(self.julia,z,c,self.power,self.itr,self.limit,self.transform)

                pass

            return



#run(100,100,0,True)
#superset(10, 100, 100, 40)
#Fractale()
