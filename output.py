class PPX(object):


    header = 3
    mode = True
    content = 0
    width = 50
    height = 50
    comment='Godiva. Fractal. Popcorn.'
    fname="Output"
    depth=8
    ext = ".pbm.pgm.ppm"

    row = 1
    
    def __init__(self):

        ppmHeader = ("P"+str(self.header + (3 if self.mode else 0))+"\n"+
                     "#"+self.comment+"\n"+str(self.width)+" "+str(self.height)+
                     "\n")

        if self.header > 1: ppmHeader += str((2**self.depth)-1)+"\n"
        

        if self.mode: #binary PPMs

            self.file = open(self.fname+self.ext[(self.header-1)*4:
                                                 self.header*4],'wb')

            self.file.write(bytearray(ppmHeader,'UTF-8'))

        else:

            self.file = open(self.fname+self.ext[(self.header-1)*4:
                                                 self.header*4]+'.txt','w')

            self.file.write(ppmHeader)


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



#a = PPX();a.setMost(1,1,3,3,'k');a.write([1,0,1]);a.write([1,0,1]);a.write([0,1,0])

##        file.write("\n")
##
##        
##    #TODO: make function recalculate colour values if incoming colour depth
##    # != depth
##    '''Basic PPM output function
##        HEADER = 1 : Portable Byte Map, 2 : Protable Greymap, 3 : Portable Pixmap
##        MODE = False : ASCII, True : Binary
##        CONTENT = Mode == False : List of Strings in PPM format,
##        --------True : List of Ints, same.
##        WIDTH, HEIGHT = width and height of image
##        FNAME = Optional file name
##        DEPTH = colour depth in bits
##    '''
##
##    '''PPM format = a 0 or 1 for each pixel if PBM, a number from 0 to 255 for each
##       pixel if PGM, or a triplet of RGB vals from 0-255 if PPM. These last should
##       be in a 1D list, that is, [255,0,0,0,255,0] for a 2x1 image containing a red
##       pixel and a green one.
##    '''
##
##     #valid extensions
##    
##
##
##        
##
##        
##
##def OLDtoPPX(header,mode,content,width,height,
##          comment='Godiva. Fractal. Popcorn.',fname="Output",depth=8):
##
##    #TODO: make function recalculate colour values if incoming colour depth
##    # != depth
##    '''Basic PPM output function
##        HEADER = 1 : Portable Byte Map, 2 : Protable Greymap, 3 : Portable Pixmap
##        MODE = False : ASCII, True : Binary
##        CONTENT = Mode == False : List of Strings in PPM format,
##        --------True : List of Ints, same.
##        WIDTH, HEIGHT = width and height of image
##        FNAME = Optional file name
##        DEPTH = colour depth in bits
##    '''
##
##    '''PPM format = a 0 or 1 for each pixel if PBM, a number from 0 to 255 for each
##       pixel if PGM, or a triplet of RGB vals from 0-255 if PPM. These last should
##       be in a 1D list, that is, [255,0,0,0,255,0] for a 2x1 image containing a red
##       pixel and a green one.
##    '''
##
##    ext = ".pbm.pgm.ppm" #valid extensions
##    
##    if mode: #binary PPMs
##
##        ppmHeader = ("P"+str(header+3)+"\n"+"#"+comment+"\n"+str(width)
##                     +" "+str(height)+"\n")
##
##        if header > 1: ppmHeader += str((2**depth)-1)+"\n" 
##
##        file = open(fname+ext[(header-1)*4:header*4],'wb')
##
##        file.write(bytearray(ppmHeader,'UTF-8'))
##
##        if header == 1:
##
##            concatenatedBits = [] #Store PBM output
##            i = 0
##            incr = 8
##
##            bytelen = width//8
##            lastbyte = width%8
##            
##            while i < len(content):
##
##                    incr = 8
##                    out = 0
##                    offset = 7 #used in bit construction to determine the value of a
##                               #given input
##
##                    if i%width != 8*bytelen:
##                        
##                        for j in range(8): #for this byte
##
##                            out += content[i+j]*2**offset #multiply incoming 1s and 0s 
##                            offset -= 1                   #by a relevant power of two,
##                                                          #and add them to the accumulator
##
##                        concatenatedBits += [out]
##                        i += incr
##
##                        
##                    else:
##
##                        #The last byte of a pbm file contains trailing zeroes if the
##                        #marginal width of the file is not divisible by eight. This
##                        #condition handles that.
##                        
##                        for j in range(lastbyte):
##
##                            out += content[i+j]*2**offset
##
##                            offset -= 1
##
##                        concatenatedBits += [out]
##
##                        i += lastbyte
##
##            #Finally, output the file.
##            file.write(bytes(concatenatedBits))
##
##        else: file.write(bytes(content)) #PGMs AND PPMS ARE SO EASY
##            
##        file.close()
##        
##    else: #ASCII PPMs. Slow.
##
##        ppmHeader = "P"+str(header)+"\n"+str(width)+" "+str(height)+"\n"
##
##        if header > 1: ppmHeader += str((2**depth)-1)+"\n"
##
##        file = open(fname+ext[(header-1)*4:header*4],'w')
##
##        file.write(ppmHeader)
##
##        for i in range(len(content)):
##            
##            file.write(str(content[i])+" ")
##
##            if (header == 3) and (i == width*3-1): file.write("\n")
##
##            elif (header <3) and  (i == width-1): file.write("\n")
##
##        file.close()



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