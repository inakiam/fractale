from datetime import datetime

class PPX(object):

    header = 3
    mode = True
    content = 0
    width = 50
    height = 50
    comment='Godiva. Fractal. Popcorn.'
    fname="Output"
    timestamp = str(datetime.now()).replace(":",".")
    depth=8
    ext = ".pbm.pgm.ppm"

    row = 1
    
    def __init__(self):

        ppmHeader = ("P"+str(self.header + (3 if self.mode else 0))+"\n"+
                     "#"+self.comment+"\n"+str(self.width)+" "+str(self.height)+
                     "\n")

        if self.header > 1: ppmHeader += str((2**self.depth)-1)+"\n"
        

        if self.mode: #binary PPMs

            self.file = open(self.timestamp+" "+self.fname+self.ext[(self.header-1)*4:
                                                 self.header*4],'wb')

            self.file.write(bytearray(ppmHeader,'UTF-8'))

        else:

            self.file = open(self.fname+self.ext[(self.header-1)*4:
                                                 self.header*4]+'.txt','w')

            self.file.write(ppmHeader)

    def setSize(self,dpi,w,h):
        '''figure out minimum size in pixels to achieve dpi wanted
        w and h are ASPECT RATIOS.'''
        pass#make this call setMost with width/height equal to  whatever is necessary to satisfy dia reqs

    def setMost(self,header,mode,width,height,fname):

        self.header = header
        self.mode = mode
        self.width = width
        self.height = height
        self.fname = fname

        self.__init__()

    def write(self,content):

        if self.mode:

            if self.header == 1:

                concatenatedBits = [] #Store PBM output
                i = 0
                incr = 8

                bytelen = self.width//8
                lastbyte = self.width%8
                
                while i < len(content):

                        incr = 8
                        out = 0
                        offset = 7 
                                   
                        if i%self.width != 8*bytelen:
                            
                            for j in range(8): #for this byte

                                out += content[i+j]*2**self.offset 
                                offset -= 1                   
                                                             

                            concatenatedBits += [out]
                            i += incr

                            
                        else:
                            
                            for j in range(lastbyte):

                                out += content[i+j]*2**offset

                                offset -= 1

                            concatenatedBits += [out]

                            i += lastbyte

               
                self.file.write(bytes(concatenatedBits))

            else: self.file.write(bytes(content)) 

        
        else: #ASCII PPMs. Slow.

            for item in content:
                
                self.file.write(str(item) + " ")

        if self.row == self.height: self.file.close()
        self.row += 1

''' NEW DEV TARGET: Since the renderer can give all julias intact; make a progream for outputting julia mosaics. '''
'''DISTANCE COLOUR ALGO. SET Z = FURTHEST POINT FROM CENTRE TO BE RENDERED. LET ANY POINT ABS(Z) BE 50% GREY.
THEN INFINITY IS WHITE, AND ZERO IS BLACK. MAybe acomplishable with a fraction with preset numerator??? Set numer = a(z)
let denom be a(z), but raise a(z) to negative power st @ infinity, div by 0, at 0, div by infinity.
'''

################## This. This needs to be translated into a procedure that Output can use to mirror the file itself.
        ########## Now that I've switched to streaming the fractal to file.
# def symmetry(rawIn, julia, yNow, yFinal, x):
#     '''Return a rotated or mirrored version of input.'''
#
#     output = []
#
#     yNow += 1
#
#     if julia:
#
#         # Julias that are symmetrical show rotal symmetry,
#         # so they need a different algorithm
#
#         for i in range(-1, (-x * 3 * (yFinal - yNow)), -3):
#             output += [rawIn[i - 2], rawIn[i - 1], rawIn[i]]
#
#
#     else:
#
#         # copy rawIn, in order, to an array, packing it by line
#         # then use extended list slicing to invert the order.
#         intermediate = [[rawIn[nums + rows] for nums in range(x * 3)]
#                         for rows in range(0, (x * 3 * (yFinal - yNow)), x * 3)][::-1]
#
#         for i in range(len(intermediate)):
#             output += intermediate[i]
#
#     return output