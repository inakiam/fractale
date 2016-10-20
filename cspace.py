from math import pi,ceil

class CSpace(object):

    default = None

    def __init__(self):

        self.rgb = self.default
        self.hsv = self.default
        self.hsl = self.default
        self.cmyk = self.default

    def setRGB(self,RGB):

        self.rgb = RGB

    def setHSV(self,HSV):

        self.hsv = HSV

    def mcRGB(self):
        '''Generate All Coordinates From RGB'''
        pass

    def rgb2hsv(self):

        rgbMax = max(self.rgb)
        rgbMin = min(self.rgb)
        chroma = rgbMax-rgbMin

        modulus = self.rgb.index(rgbMax)

        if chroma == 0:
            hue = False
        else:
            hue = self.rgb[(modulus+1)%3]-self.rgb[(modulus+2)%3]
            hue /= chroma

            if modulus == 0:
                hue %= 6
            elif modulus == 1:
                hue += 2
            elif modulus == 2:
                hue += 4

            hue *= 60#(pi/3)

        self.hsv = [hue,0 if not(chroma) else chroma/rgbMax,rgbMax]

        return self.hsv

    def hsv2rgb(self):

        reRGB = [0,0,0]

        if self.hsv[0] is False:
            self.RGB = reRGB
            return self.RGB

        chroma = self.hsv[1] * self.hsv[2]
        rgbMin = self.hsv[2] - chroma

        unhue = self.hsv[0]/60        
        
        dichroma = chroma * (1 - abs(unhue%2 - 1))

        reRGB = [0,0,0]

        for i in range(6):
            if i <= unhue < i+1:
                #Screw nested ifs, amirite
                #See wikipedia, "HSL & HSV"
                reRGB[ceil(i/2)%3] = chroma
                reRGB[ceil(-i+1/2)%3] = dichroma
                reRGB[ceil((3+i)/2)%3] = 0

        self.rgb = [ceil(colors+rgbMin) for colors in reRGB]
        
        return self.rgb


