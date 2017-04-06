# cTools.py
# set of useful concepts for working with graphs

from decimal import *
from math import *

getcontext().prec = 10000
from random import *


def error(a, b):
    out = []

    for i in b:
        lt = -1
        gt = -1

        for j in a:

            if j <= i:
                lt = j
            elif j > i:
                gt = j
                break

        ltDif = i - lt
        gtDif = gt - i

        out += [gtDif if gtDif >= ltDif else ltDif]

    return out


def gen():
    n = 30030

    factors = [2, 3, 5, 7, 11]
    powers = [1, 1, 1, 1, 1]

    first = 0

    out = -1

    output = []

    while out != first:
        out = 0
        for i in range(len(factors)):
            num = factors[i] ** powers[i]
            out += num if num < n else num / factors[i]
            powers[i] = powers[i] + 1 if num < n else 0

        output += [out]

    print("done")
    return output


def thing(itr, size):
    iterCount = []

    iSet = set()

    for i in range(itr):

        ic = 0
        while len(iSet) < 10 ** size:
            iSet.add(randint(0, 10 ** size - 1))
            ic += 1

        iterCount += [ic]
        iSet.clear()

    return iterCount


def pe(n):
    def prod(n):
        out = 1
        for i in n: out *= i
        return out

    a = sieve(n)
    b = [prod(a[0:i + 1]) for i in range(len(a))]
    c = [Decimal(i) ** -1 for i in b]

    return sum(c)


def pre(n):
    def prod(n):
        out = 1
        for i in n: out *= i
        return out

    a = [i for i in range(1, n + 1)]
    b = [prod(a[0:i + 1]) for i in range(len(a))]
    c = [Decimal(i) ** -1 for i in b]

    return 1 + sum(c)


def ne(n):
    def prod(n):
        out = 1
        for i in n: out *= i
        return out

    ax = sieve(n)
    ay = [i for i in range(1, n + 1)]

    a = [i for i in ay if i not in ax]
    b = [prod(a[0:i + 1]) for i in range(len(a))]
    c = [Decimal(i) ** -1 for i in b]

    return 1 + sum(c)


def invConsts(n):
    '''Calculate sum of inverse powers of n.'''

    getcontext().prec = 400

    out = 0

    for i in range(4000):
        out += Decimal(n) ** Decimal(-(i + 1))

    return out


def toPPX(header, mode, content, width, height,
          comment='Godiva. Fractal. Popcorn.', fname="Output", depth=8):
    # TODO: make function recalculate colour values if incoming colour depth
    # != depth
    '''Basic PPM output function
        HEADER = 1 : Portable Byte Map, 2 : Protable Greymap, 3 : Portable Pixmap
        MODE = False : ASCII, True : Binary
        CONTENT = Mode == False : List of Strings in PPM format,
        --------True : List of Ints, same.
        WIDTH, HEIGHT = width and height of image
        FNAME = Optional file name
        DEPTH = colour depth in bits
    '''

    '''PPM format = a 0 or 1 for each pixel if PBM, a number from 0 to 255 for each
       pixel if PGM, or a triplet of RGB vals from 0-255 if PPM. These last should
       be in a 1D list, that is, [255,0,0,0,255,0] for a 2x1 image containing a red
       pixel and a green one.
    '''

    ext = ".pbm.pgm.ppm"  # valid extensions

    if mode:  # binary PPMs

        ppmHeader = ("P" + str(header + 3) + "\n" + "#" + comment + "\n" + str(width)
                     + " " + str(height) + "\n")

        if header > 1: ppmHeader += str((2 ** depth) - 1) + "\n"

        file = open(fname + ext[(header - 1) * 4:header * 4], 'wb')

        file.write(bytearray(ppmHeader, 'UTF-8'))

        if header == 1:

            concatenatedBits = []  # Store PBM output
            i = 0
            incr = 8

            bytelen = width // 8
            lastbyte = width % 8

            while i < len(content):

                incr = 8
                out = 0
                offset = 7  # used in bit construction to determine the value of a
                # given input

                if i % width != 8 * bytelen:

                    for j in range(8):  # for this byte

                        out += content[i + j] * 2 ** offset  # multiply incoming 1s and 0s
                        offset -= 1  # by a relevant power of two,
                        # and add them to the accumulator

                    concatenatedBits += [out]
                    i += incr


                else:

                    # The last byte of a pbm file contains trailing zeroes if the
                    # marginal width of the file is not divisible by eight. This
                    # condition handles that.

                    for j in range(lastbyte):
                        out += content[i + j] * 2 ** offset

                        offset -= 1

                    concatenatedBits += [out]

                    i += lastbyte

            # Finally, output the file.
            file.write(bytes(concatenatedBits))

        else:
            file.write(bytes(content))  # PGMs AND PPMS ARE SO EASY

        file.close()

    else:  # ASCII PPMs. Slow.

        ppmHeader = "P" + str(header) + "\n" + str(width) + " " + str(height) + "\n"

        if header > 1: ppmHeader += str((2 ** depth) - 1) + "\n"

        file = open(fname + ext[(header - 1) * 4:header * 4], 'w')

        file.write(ppmHeader)

        for i in range(len(content)):

            file.write(str(content[i]) + " ")

            if (header == 3) and (i == width * 3 - 1):
                file.write("\n")

            elif (header < 3) and (i == width - 1):
                file.write("\n")

        file.close()


def slider(resetX, resetY, locX, locY, step, setXTo=0, setYTo=0):
    '''Function to iterate through all points on a given 2D grid
    with arbitrary starting coordinates.
    reset  = the highest valid coord
    locX/Y = position on a given axis
    setTo = the first coordinate to calculate from'''

    x = locX + step

    if x >= resetX and locY < resetY:  # if x is at reset, but y is less than
        x = setXTo
        y = locY + step
        # reset the position of x and move down a row
    else:
        y = locY

    if y >= resetY: y = setYTo

    return x, y


# Pallet Smoother
def smoothIt(pallet, r=0):  # R = NUMBER OF RECURSIONS

    pal = []

    for i in range(len(pallet)):
        pal += pallet[i]

    pT = pal[3:] + pal[:3]

    intermediates = [(pal[i] + pT[i]) // 2 for i in range(len(pal))]

    smoothed = []

    for i in range(0, len(pal), 3):
        smoothed += [[pal[i], pal[i + 1], pal[i + 2]]]
        smoothed += [[intermediates[i], intermediates[i + 1], intermediates[i + 2]]]

    if r > 0:
        smoothed = smoothIt(smoothed, r - 1)

    return smoothed


# Generalised numeric base conversion.
# useful for encoding large binary numbers as smaller symbols

def tBaseN(message, n=2048):
    # Convert stupidly large numbers into something managable

    # Make a dictionary that relates numbers to Hanzi
    codeTable = {i - 19968: chr(i) for i in range(19968, 19968 + n)}

    digest = []

    while True:

        # Convert message to Base-n
        # Hanzi = digits

        digest += [codeTable[message % n]]

        if message // n == 0:
            break

        message //= n

    return ''.join(digest)[::-1]


def fBaseN(message, n=2048, base=False):
    # Create table relating Hanzi to numbers
    codeTable = {chr(i): i - 19968 for i in range(19968, 19968 + n)}

    # create array of place values of digested number, if they were all ones
    digest = [codeTable[i] for i in message][::-1]
    # also, reverse it, since we want to eat the lowest pv first

    # Results accumulator
    final = 0

    for i in range(len(digest)):
        final += digest[i] * (n ** i)
        # multiply ones by their actual place values and accumulate the total

    if base:  # delete this

        final = tBaseN(final, base)
        final = fBaseN(final, base)

    return final


# Naturally Formatted Complex Numbers

def toComplex(inStr):
    inStr = inStr.split(',')

    inStr[1] = inStr[1][:len(inStr[1]) - 1] + 'j'

    if inStr[1][0] != '-':
        inStr[1] = '+' + inStr[1]

    output = ''.join(inStr)

    return complex(output)


def fComplex(inComplex):
    # Bugged: Cannot parse comps w/ a real part of 0.

    if inComplex.real == 0 and inComplex.imag > 0:
        conversionConst = "0+"
    else:
        conversionConst = "0"

    # Typecast inComplex to str; handle cases where real part == 0.
    inComplex = (conversionConst + str(inComplex) if inComplex.real == 0
                 else str(inComplex))

    inComplex = inComplex[1:len(inComplex) - 2] + 'i'

    inSign = inComplex.find('-') if inComplex.find('-') != -1 else \
        False

    if not inSign:

        output = ','.join(inComplex.split('+'))

    else:

        output = inComplex[:inSign] + ',' + inComplex[inSign:]

    return output


def count(s):
    acc = {}

    for i in s:

        try:
            acc[i] += 1

        except:
            acc[i] = 1

    return acc


def ci(a, l):
    a = [111, 121, 134, 154, 156, 200, 222, 143, 165, 217]

    n = len(a)
    sA = sum(a)
    µ = sA / n

    sAA = [a - µ for i in a]

    stDev = sqrt(sAA ** 2 / n)

    err = 0.5 * l * stDev / sqrt(n)


def mn(a):
    return sum(a) / len(a)


def okk(s):
    s = s.replace(',', '').replace(' ', '').replace('!', '').replace('?', '')
    s = ["0" if i is "o" else "1" for i in s.lower()]
    s = [int(''.join(s[i:i + 8])) for i in range(0, len(s), 8)]

    return s


def add(a, b, rad=2):
    l = [len(a), len(b)]
    s = list("0" * (1 + l[0] if l[0] > l[1] else 1 + l[1]))
    d = 1

    rad = {i: str(i) for i in rad}

    if l[0] < l[1]:
        a = "0" * (l[1] - l[0]) + a
    elif l[1] < l[0]:
        b = "0" * (l[0] - l[1]) + b

    def pv(num, summ, i):

        if (num[i] is "1") and (summ[i] is "1"):

            p = "1"
            while p is "1":
                summ[i] = "0"

                if summ[i - 1] is "1":
                    i -= 1
                else:
                    summ[i - 1] = "1"
                    p = "0"

        elif (num[i] is "1") and (summ[i] is "0"):
            summ[i] = num[i]

        return summ

    for i in range(-1, -(len(a) + 1), -1):
        s = pv(a, s, i)
        s = pv(b, s, i)
        d = i if s[i] is "1" else i - 1 if s[i - 1] is "1" else d

    d = d if d < 1 else -1

    return ''.join(s[d:])


def dirReduc(arr):
    names = {'NORTH': 1, 'SOUTH': -1, 'EAST': 2, 'WEST': -2}
    complete = False

    while not (complete):

        for i in range(len(arr) - 1):
            if names[arr[i]] + names[arr[i + 1]] == 0:
                arr = arr[:i] + arr[i + 2:]
                break

            if i + 1 == len(arr) - 1:
                complete = True

        if len(arr) == 1 or len(arr) == 0: complete = True

    return arr


def sieve(ceiling):  # Sieve of Eratosthenes

    primes = [2]
    prime = True

    for i in range(2, ceiling):

        for j in primes:
            if i % j == 0:
                prime = False

        if prime:
            primes += [i]

        prime = True

    return primes


def geo(ceil, pump):
    return [i ** pump for i in range(1, ceil)]


def e(precis):
    e = Decimal(0)
    x = Decimal(1)

    for i in range(precis):

        for j in range(i):
            x *= Decimal(j + 1)

        e += Decimal(1 / x)
        x = Decimal(1)

    return e


def going(n):
    def prod(x):
        n = 1
        for i in x: n *= i
        return n

    n = [i for i in range(n + 1)][1:]
    n = [prod(n[:i + 1]) for i in range(len(n))]
    inv = 1 / n[-1]

    return sum(n) * inv


def factorial(n):
    out = 1
    for i in range(1, n):
        out = 1 * out * (i + 1)
    return out


def itfact(n, rec):  # turn cpu into space heater
    m = n
    for i in range(itfact(m, rec - 1) if rec != 0 else n):
        m = factorial(m)
    return m


def progress(n, final=190, temp=290, orig=315, begin=360):
    fromStart = begin - n
    fromNew = orig - n
    toTemp = n - temp
    toFinal = n - final
    fSTT = toTemp / fromStart
    fSTF = toFinal / fromStart
    fOTT = toTemp / fromNew
    fOTF = toFinal / fromNew

    print(fSTT, fSTF, fOTT, fOTF)


def arborial(arbs):
    a = 1

    for i in arbs: a *= i

    return a


def gdigs(digits, base):
    x = base

    for i in range(digits):
        x = pow(base, x, 10 ** digits)

    return "0%d" % x


# Makes sure a given string will be as long as scandepth by adding leading 0's

lFormat = lambda x: ('0' * (0 - len(x)) + x)  # Deprecated.
