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

def allComplexRoots(z, n):
    '''Get all complex roots of z.'''
    nthRootOfr = abs(z)**(1.0/n)
    t = phase(z)
    return [map(lambda k: nthRootOfr*exp((t+2*k*pi)*1j/n), range(n))]

def allComplexLogs(z):
    '''Get all complex logs of z.'''


def iMeanIt(nList, mType):
    '''Returns various types of mean.'''

    if type(nList[0]) is int: #if nList is escTime, so geomean is nonzero
        #This is OK because it's OK to count from 1. If ugly.
        nList = [i + 1 for i in nList]

    if mType == 0: #Arithmetic
        return (sum(nList) / len(nList))
    if mType == 1: #Geometric
        gMean =  (prod(nList) ** (1 / len(nList)))

        return gMean - 1 if type(nList[0]) is int else gMean
    if mType == 2: #Harmonic
        return len(nList) * sum([i ** -1 for i in a]) ** -1

def prod(n):
    out = 1
    for i in n: out *= i
    return out

def pe(n):

    a = sieve(n)
    b = [prod(a[0:i + 1]) for i in range(len(a))]
    c = [Decimal(i) ** -1 for i in b]

    return sum(c)


def pre(n):


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


def e(precis):
    e = Decimal(0)
    x = Decimal(1)

    for i in range(precis):

        for j in range(i):
            x *= Decimal(j + 1)

        e += Decimal(1 / x)
        x = Decimal(1)

    return e

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


def arborial(arbs):
    a = 1

    for i in arbs: a *= i

    return a


def gdigs(digits, base):
    x = base

    for i in range(digits):
        x = pow(base, x, 10 ** digits)

    return "0%d" % x