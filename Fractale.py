from cmath import *
##Custom Classes
from colouring import Colouring
from graph import Graph
from output import PPX
from eqs import Formula
# Custom Functions
from cTools import *



# Builtin Functions

# Whole libs

# Initialize Objects

plane = Graph()
field = Graph()
colour = Colouring()
formula = Formula()


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

def calculate(fSet, pwr, itr, julia, zBase, cBase, opt, resX, resY, n, raw):
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
    formula.setFormula(fSet)

    # Iterate over the space.
    for y in range(resY):

        for x in range(resX):

            c = complex(plane.posX, plane.posY) + cBase
            z = zBase

            z = formula.read(julia, z, c, pwr, itr, limit)

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
    calculate(fSet, 2, 80, j, (.1 + .2j), (0 + 0j), False, x, y, " Raw ", False)
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
    mSet = False
    curLine = []
    outp = PPX()
    outp.setMost(3, 1, x, y, 'SuperOutput')
    color.updateMulti(pal=0)
    cOut = color.cPic(3)
    cIn = [0, 0, 0]

    for rows in range(y):

        for points in range(x):
            zIn,zOut = calculate(formSet, 2, itr, mSet, complex(field.posX, field.posY)
                          , complex(cX, cY), False, j, j, "", True)


            escAvg = sum([i[1] for i in zOut]) / j ** 2
            zAvg = sum([i[0] for i in zOut]) \
                   / j**2
            

            curLine += cOut([zAvg], complex(escAvg), 0, 0)

            field.posX += field.fsX

        # Satisfy idle curiosity
        if rows % 15 == 1: print('Render is', str(round((rows / y) * (2 if sSym else 1)
                                                        * 100, 3)) + '% done.')
        outp.write(curLine)
        field.posY += field.fsY
        field.posX = field.reset[0]

        curLine = []

    print("Render complete.")

class Fractale(Graph):

    #Default values
    ##Mandel/Julia Switch
    baseSetMandel = True

    ##Iteration Depth
    itr = 80
    ##Bailout Value: Stop calculation when abs(z) exceeds.
    limit = 4

    ##Base values of z,c
    zBase = 0j
    cBase = 0j

    ##Coordinate Transform
    transform = lambda c: c

    ##Fractal set id
    Eqs = formulas(transform)
    ##power of set
    power = 2



    ##Image Resolution
    resX = 100
    resY = 100

    ##Point Generation Algorithm
    algo = 1
    # 0 = Graph
    # 1 = Roots
    ##Rendering Method.
    rMode = min(algo,1)

    def __init__(self,base=True,antecedent = None):

        #Setup Graph...
        self.Plane = Graph()
        self.Plane.updateMulti(resX=self.resX, resY=self.resY, epicentre=[-.75, 0], magnitude=0)


        #Inconstants
        if base:
            #create things not necessary in recursive calculators
            self.superCalc = Fractale(False,self)

            #file output
            self.out = PPX()
            self.out.setMost(3,1,self.resX,self.resY,'Fractale [' +str(tBaseN(randint(1,4000))) + ']')

            #Colouring not required by recursive class...
            self.Colour = Colouring()
            self.cIn = self.Colour.cPic(0)
            self.cOut = self.Colour.cPic(3)

            #Output var to be used if the dataset is being saved for later processing...
            self.rOut = []
        else:
            #Give supercalc access to Parent
            self.Parent = antecedent

            #What type of thing is superset pixels?
            self.baseSetMandel = not(self.Parent.baseSetMandel)

            #autoconfigure sSet render with some defaults...
            self.algo = self.Parent.algo
            self.rMode = min(self.algo, 1)
            self.resX = 10
            self.resY = 10


            #Make vars not needed in Base instance.
            self.output = [[],[]] #[inside set],[out]

    def __genCloud__(self,c):
        '''Generates a number of roots ~= julia pixelres.'''

        out = []

        #There are n nth roots, thus a sum of root is the n sumorial.
        #Find closest sumorial number jpixelres
        sumorial = round(.5 * (1 + (8 * (self.resX * self.resY) + 1) ** .5))

        for i in range(1, sumorial + 1):
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

    def setbaseRMode(self,mode):
        self.rMode = mode

    def render(self):

        #raw output var


        if self.rMode == 0:

            for y in range(self.resY):

                curLine = []

                for x in range(self.resX):

                    c = complex(self.Plane.posX, self.Plane.posY)
                    z = self.zBase

                    z = self.Eqs.read(self.baseSetMandel,z,c,self.power,self.itr,self.limit)

                    escTime = len(z) - 1

                    if self.algo == 0:
                        if escTime == self.itr:
                            curLine += self.cIn(z, escTime, self.itr, c)
                        else:
                            curLine += self.cOut(z, escTime, self.itr, c)
                    elif self.algo == 1:
                        if escTime == self.itr:
                            self.output[0] += [[z[-1], escTime]]
                        else:
                            self.output[1] += [[z[-1], escTime]]
                    else: self.rOut += [z]

                    self.Plane.posX += self.Plane.fsX

                self.Plane.posX = self.Plane.reset[0]
                self.Plane.posY += self.Plane.fsY

                if self.algo == 0:
                    self.out.write(curLine)
                    curLine = []

            #Return Values for graph renders...
            if self.algo == 1:
                return self.output
            elif self.algo == 3:
                return self.rOut
            else:
                return -1

             #algo == 1
        elif self.rMode == 1 and not(self.baseSetMandel): # this rendermode makes no sense for base sets

            pointCloud = self.__genCloud__(self.c)

            for c in pointCloud:

                z = self.Eqs.read(self.baseSetMandel,z,c,self.power,self.itr,self.limit)
                escTime = len(z) - 1

                if escTime == self.itr:
                    self.output[0] += [[z[-1], escTime]]
                else:
                    self.output[1] += [[z[-1], escTime]]


            return self.output



#run(100,100,0,True)
#superset(10, 100, 100, 40)
#f = Fractale()
#f.render()
