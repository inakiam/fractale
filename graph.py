#graph.py
#Resolution-independent graph object.
#maps the positive-only coordinate-system of images
#to the complex plane


class Graph(object):

    #External resolution vars
    resX = 200
    resY = 200

    #Graph Limit Vars
    epicentre = [0,0] #Central coordinates.
    magnitude = 0 #Zoom.
    start = 2 #Edges if magnitude == 0.

    def __init__(self):

        '''Generate a resolution-independent graph.'''

        #Translation Var
        zoom = 2**self.magnitude

        #Begin Calculated Vars.

        ##Graph Limit Vars

        base = self.start/zoom
        
        #### X coords
        xlPos = base + self.epicentre[0]
        xlNeg = -base + self.epicentre[0]
        
        ####Y coords
        ylPos = base + -self.epicentre[1]
        ylNeg = -base + -self.epicentre[1]

        #Calculate how much the point increments

        fSx = (abs(xlNeg)+xlPos)/self.resX
        fSy = (abs(ylNeg)+ylPos)/self.resY

        ##Use smaller number, prevent magnification glitches
        self.fundamentalStep = fSx if fSx <= fSy else fSy

        ##Generate final steps
        self.fsX = self.fundamentalStep
        self.fsY = self.fundamentalStep

        #Resolution independence. Change GL vars to account for inequalty of
        #long and short sides, if extant.
        
        if self.resX != self.resY:

            #Determine how much shorter the side is in terms of fS, divide by 2
            #because half is given to the left/bottom, the other to the
            #right/top
            
            inequality = ((self.resX - self.resY if self.resX > self.resY
                           else self.resY - self.resX)*self.fundamentalStep)/2

            if self.resX > self.resY:

                ylNeg += inequality
                ylPos -= inequality

            else:

                xlNeg += inequality
                xlPos -= inequality

        #Render Point Vars. Track position of reading head.

        self.posX = xlNeg
        self.posY = ylNeg

        ## Reset var for when head goes out of range.
        self.reset = [xlNeg,ylNeg]

        #Var containing epicentre, a corner, and .
        #Useful for various distance calcs
        self.centralExtrema = ((xlNeg,ylNeg), (self.epicentre[0],self.epicentre[1]))

    #Update functions: Change some info about graph and get new units.
    #Enables resizing window, moving udlr, and zooming

    def updateRes(self,x,y):
        
        self.resX = x
        self.resY = y

        self.__init__()

    def updateEp(self,epicentre):

        self.epicentre = epicentre

        self.__init__()

    def updateStart(self,start):

        self.start = start

        self.__init__()

    def updateMag(self,magnitude):

        #Magnitude doubles when zoom doubles, but it's more intuitive for
        #the UI to use a slider that increases by 1 per doubling. Thus...

        self.magnitude = magnitude

        self.__init__()

    def updateMulti(self,**kargs):

        '''Multi-argument update function.'''
        #Valid names are resX, resY, epicentre, magnitude, start.

        for i in kargs: setattr(self,i,kargs[i])

        self.__init__()