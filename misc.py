#mathtricks.py
#collection of useful functions that were not built in.
#prolly cause they're fucking stupid.


#The Fractional Absolute Value Quartet

def fabs(n,fraction):

    '''Determine fractional absolute value.'''
    #Main use is for contorting mandelbrot into
    #burning ship over the course of a for loop.

    #remeber to eventually benchamrk this comparison vs giving complex ns their
    #own function which calls fabs

    if type(n) is not complex:

        if n < 0:

            #For this to work, -5 will need to = 5 if fraction = 1/1.
            #But 1/1 * abs(-5) = 5, which only gets us to zero, hence,
            #each movement needs double the increment given to yield
            #correct motion.
            fraction = fraction * 2

            return n + abs(n) * fraction

        else:

            #Positive numbers are their own absolutes. No motion.
            return n


def cfabs(n,fraction):

    #If not impossible, you should really just do this directly and save the
    #function call.

        realFabs = fabs(n.real,fraction)
        imagFabs = fabs(n.imag,fraction)

        return complex(realFabs,imagFabs)


def invfabs(n,fraction):

    '''Alter operation of fabs so its action is mirrored.'''

    if n > 0:

        return (fabs(n*-1,fraction)*-1)

    else:

        return fabs(n,fraction)

def cinvfabs(n,fraction):

    #Seriously.

        realFabs = invfabs(n.real,fraction)
        imagFabs = invfabs(n.imag,fraction)

        return complex(realFabs,imagFabs)

def swap(n):

    return complex(n.imag,n.real)
