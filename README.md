# fractale

Fractale is a fractal fractal calculator calculator designed by me for the sole putpose of doing things other calculators won't let me do without paying for them. The main use case is the creation of so-called fractal supersets, which are awesome images made by compressing julia sets into pixels to create maps of juliaspace. 

I don't particularly care about how nice looking the codebase is, so prepare for your eyes to bleed on the sheer amateur-hour-ness of it.


#Documentation

THIS DOCUMENTATION IS WRITTEN FOR A LATER VERSION. FRACTALE DOES NOT YET WORK.


##Writing a custom formula

You can use the follwing variables:

z, c, and p

If you are multiplying, always type the "\*" explicitly! Algebraic expression of coefficients is not *yet* supported. If you write 2(z) or 2z, it won't work.

Typing "x" to multiply will *never* be supported. Typing 2xZ will cause an error. Type 2\*Z

Spaces are OK. The program can deal with them.

If you want to write a power, "^" and "\*\*" are supported. z\*\*2 and z^2 wll both square z.

Some extra functions are supporte:

*The three main trig functions - sin, cos, tan - and their hyperbolic equivalents, as will as the inverse functions of all of those
*Natural logartihm w/ log(number)
**Unnatural log via log(number,base) - may cause accusations of blasphemy
*exp and sqrt, if you want them
*Some useful constants - pi, e,

##Animating

When you give a formula to Fractale, it breaks it down into a number of terms. A term is any item in the statement separated from any other item by an addition. For example, the formula "Z + C" has two terms: Z, and C.

Terms can have subterms. Subterms are any items inside parentheses, even if you are using the parentheses as notational decorations. An example: z + sin(z) has two terms - z, and sin(). sin() has the subterm z. Fractale will also interpret z + (z) as a two-term formula, with terms z and () and () having the subterm z

Terms and subterms have adresses. These adresses count from zero.

Example:

    Formula:    z^2 + z + cos(c - tan(z))
    Term Addr:  0     1   2   2   2   2
                              .   .   .
    						  0   1   1
    								  .
    								  0
    
So, to refer to the z inside tan(z) by adress, you call it term 2.1.0

This numerical adress system is used because it gives every part of the equation a unique address. This means you can refer to term 1 - "z" and term 2.1.0 (also "z") separately. This grants you total fine control over the contents of the formula.

To animate the fractal, you transform the formula over time. In the future, cuesheet files will be supported for this. For the time being, do so by using the AddAnim function. The format for this function is a string containing the address of the term you want to alter, and a list of tuples containing the specifications for the alterations.

The tuples are formatted as follows:

(term, interpolationMethod, startTime, endTime)

The term is just a string containing what you want the element to change to.

The interpolation method is how you want Fractale to transform the term into the other. Two methods are presently supported - linear, and trigonometric. THese are discussed in detail at the end of this segment.

The start time tells fractale when it should start the transformation. The start time of at least *one* transformation in your animation must be zero, for now. (actually, it doesn't, but unless you want to waste time and compute resources, should make sure to do this so fractale doesn't render the same fractal 30 times in a row)

The end time tells Fractale when the transformation should be complete.

Times are specified in seconds, and while Fractale will make all due efforts to follow your instructions, in the event that the start and endtimes you entered in are not divisible by the framerate fo your video, fractale will round to the next time that *is*.

So if you shot a transformation at 4 frames per second, and specifed a transform would start at zero and end at 2.76 seconds, fractale would render eleven frames, and produce a 2.75 second video.

This behaviour is necessary to ensure every transformation actually completes in a frame that fractale renders. If the program didn't work like this, and if a transformation completed betwen rendered frames, it could seem to "snap" between complete and incomplete with noticeable jerking.

###Interpolation

Interpolation is how Fractale allows you to transform fractals. The basic concept is this - if z^2 + c is the mandelbrot set, and z̄^2 + c is the mandelbar set, then the addition of the sets is z^2 + z̄^2 + c

(We don't have 2c or c + c because the variable c represents the complex plane. z represents the fractal. We want to add the fractals, but not the plane, here.)

let's add two variables - a, and b. a will quantify *how much mandelbrot* we want, and b will quantify how much *mandelbar* we want. This gives us a * z^2 + b * z̄^2 + c.

If we set a = 2, and b = 1, we say we want twice the mandelbrot set for every one of the mandelbar we get.

This is not so useful. It becomes useful when one restrictis the range of a, and defines b in terms of a.

By restricting a to [0,1], and defining b as 1 - a, we  create a balanced tradeoff. Under this restriction and definition, a + b always equals 1. This actually fixes a loto of problems - when a + b doesn't equal 1, the fractal produced is larger or smaller than you would expect, which causes problems for rendering them.

Once a is on the interval [0,1] and b = 1-a, by increasing and decreasing the value of a by specified amounts, smooth transformations of the set become possible. All one has to do is set a = x/y, where x is how much of the fractal a is linked to, and y is how many intervals you want in the transformation, minus one. If you want a two step transformation, y should equal 1, since that gives two in-range values for x - 0 and 1.

This lets you interpolate between two fractals linearly!

Fractale basically automates this process, and allows any term to be interpolated in any way, at any time.

In addtion to this linear method, fractale also supports a sinusoidal method, which takes advantage of the fact that sin(x)^2 + 1-sin(x)^2 = 1. The sinusoidal method has a slow start, quick middle, and slow finish.

The linear method had constant speed throughout.




### Linear Transform



An example call: addAnim("3.1", [ ("z",0,0,1) , ("c/z",0,1,5) , ... , (z^log(z),1,9971,20000 ] )

This call asks the rederer to animate term 3.1. 


##License
License is WTFPL 2.0, because really, who would?


##TODO
* rewrite rendering architecture so that z is a vector of all of z's states thus allowing more colouring algos + implicit storage of c as z[0]
* create colourspace.py class for HSL-HSV-RGB-WHATEVER colour conversions.
* rewrite fractale.py architecture to be less pants-on-head stupid
