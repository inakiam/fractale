# fractale
![mandelbrot superset](https://raw.githubusercontent.com/inakiam/fractale/master/sOut.png)

Fractale is a fractal fractal calculator calculator designed by me for the sole putpose of doing things other
calculators won't let me do without paying for them. The main use case is the creation of so-called fractal supersets,
which are awesome images made by compressing julia sets into pixels to create maps of juliaspace.

I don't particularly care about how nice looking the codebase is, so prepare for your eyes to bleed on the sheer
amateur-hour-ness of it.

# "Fractal fractal renderer Renderer ?"

In addition to doing the same tired crap other fractal renderers do, fractale's renderer is recursive. It can render a
given fractal set by rendering the julia or mandelbrot sets for that set, and compiling them into a single image. The
term for such an image is a fractal superset.

THe image that you see at the top of this page provides an example of the output. It used 10x10 images of julia sets on
the interval (-2-2i,2+2i) each calculated for forty iterations to colour each pixel. The original resolution of the
banner was 4000x1250, making the actual resolution of the image 40,000 by 12,500 pixels.

As you can tell, supersets are highly computationally expensive. For this reason, the primary long-term goal of Fractale
is to move the algorithm to the GPU, since most of the usual optimizations just don't work on fractal supersets.

# Feature List of Features That Will Exist in v.01

* User Formula Input
* Smooth Colouring
* Relational Supersets
* * Root Sets
* * Log Sets
* * Others
* Fractal Animation transform 
* * Forced linear/sinusoidal speed
* * * The distance between some sets, particularly those with  higher powers of z and lower ones is not itself linear, 
so we have to renormalise that and pick values of tranforms that behave as desired.
* * Formula Transforms
* * Plane Transforms
* * With custom timing for music sync
* GPU Support
* * Probably only CUDA at first.
* Rudimentary GUI.
* Finish writing colourspace.py class for HSL-HSV-RGB-WHATEVER colour conversions.
* rewrite fractale.py architecture to be less pants-on-head stupid



# Documentation

THIS DOCUMENTATION IS WRITTEN FOR A LATER VERSION. FRACTALE DOES NOT YET WORK.


## Writing a custom formula

If you are multiplying, always type the "\*" explicitly! Algebraic expression of coefficients is not *yet* supported.
If you write 2(z) or 2z, it won't work.

Typing "x" to multiply will *never* be supported. Typing 2xZ will cause an error. Type 2\*Z

Spaces are OK. The program can deal with them.

If you want to write a power, "^" and "\*\*" are supported. z\*\*2 and z^2 wll both square z.


### Allowed Constants and Variables, and What They Do

z, c, p, a_n, and r_n, pi, and  e.

z is the principle calculated coordinate of the set, and equals 0 at iteration 0. c is the base coordinate, and is a
constant. z and c switch places in a julia set, and post swap, neither has a value of 0. p is always what z was
*on the prior iteration*. a_n is an absolute previous value of z, where n is the iteration you want. r_n is a relative
previous value of z, where, n is the number of iteration back you want.

a_n and r_n will default to an identity element supposing the index you select doesn't exist yet. For example, if you
type a_10, until iteration 10, it won't appear. If you type r_3, until you have at least three iterations,
it won't appear. But, if you're using them to multiply other things, or add, those things will appear. So basically,
until a_n or r_n has valid data, they act like 0 when added or subtracted, 1 when multiplied, etc.

Please note that this is achieved by functions, and so can meaningfully impact your rendering time. Snrk.

pi and e are the constants using those names. They are and do what you'd expect.


### Supported Functions

* The three main trig functions - sin, cos, tan - and their hyperbolic equivalents, as will as the inverse functions 
of all of those
* Natural logartihm w/ log(number)
* * Unnatural log via log(number,base) - may cause accusations of blasphemy
* exp and sqrt, if you want them
* Non-principal roots via nrootn(number,depthOfRoot,rootPhase)
* Riemann Zeta Function
* Contact me for whatever you want, or fork cTools and add it in the appropriate section.



## Animating

When you give a formula to Fractale, it breaks it down into a number of terms. A term is any item in the statement 
separated from any other item by an addition. For example, the formula "Z + C" has two terms: Z, and C.

Terms can have subterms. Subterms are any items inside parentheses, even if you are using the parentheses as notational 
decorations. An example: z + sin(z) has two terms - z, and sin(). sin() has the subterm z. Fractale will also interpret 
z + (z) as a two-term formula, with terms z and () and () having the subterm z

Terms and subterms have adresses. These adresses count from zero.

Example:

    Formula:    z^2 + z + cos(c - tan(z))
    Term Addr:  0     1   2   2   2   2
                              .   .   .
    						  0   1   1
    								  .
    								  0
    
So, to refer to the z inside tan(z) by adress, you call it term 2.1.0

This numerical adress system is used because it gives every part of the equation a unique address. This means you can 
refer to term 1 - "z" and term 2.1.0 (also "z") separately. This grants you total fine control over the contents of the 
formula.

To animate the fractal, you transform the formula over time. In the future, cuesheet files will be supported for this. 
For the time being, do so by using the addAnim function. The format for this function is a string containing the address
of the term you want to alter, and a list of tuples containing the specifications for the alterations.

Ex: addAnim("3.1", [ ("z",0,0,1) , ("c/z",0,1,5) , ... , (z^log(z),1,9971,20000 ] )

The tuples are formatted as follows: (term, interpolationMethod, startTime, endTime)

The term is just a string containing what you want the element to change to.

The interpolation method is how you want Fractale to transform the term into the other. Two methods are presently 
supported - linear, and trigonometric. These are discussed in detail at the end of this segment.

The start time tells fractale when it should start the transformation. The start time of at least *one* transformation 
in your animation must be zero, for now. (actually, it doesn't, but unless you want to waste time and compute resources,
should make sure to do this so fractale doesn't render the same fractal 30 times in a row)

The end time tells Fractale when the transformation should be complete.

Times are specified in seconds, and while Fractale will make all due efforts to follow your instructions, in the event 
that the start and endtimes you entered in are not divisible by the framerate fo your video, fractale will round to the 
next time that *is*.

So if you shot a transformation at 4 frames per second, and specifed a transform would start at zero and end at 2.76 
seconds, fractale would render eleven frames, and produce a 2.75 second video.

This behaviour is necessary to ensure every transformation actually completes in a frame that fractale renders. If the 
program didn't work like this, and if a transformation completed betwen rendered frames, it could seem to "snap" between
complete and incomplete with noticeable jerking.


### Interpolation

Interpolation is how Fractale allows you to transform fractals. The basic concept is this - if z^2 + c is the mandelbrot
set, and z̄^2 + c is the mandelbar set, then the addition of the sets is z^2 + z̄^2 + c

(We don't have 2c or c + c because the variable c represents the complex plane. z represents the fractal. We want to add 
the fractals, but not the plane, here.)

let's add two variables - a, and b. a will quantify *how much mandelbrot* we want, and b will quantify how much 
*mandelbar* we want. This gives us a * z^2 + b * z̄^2 + c.

If we set a = 2, and b = 1, we say we want twice the mandelbrot set for every one of the mandelbar we get.

This is not so useful. It becomes useful when one restrictis the range of a, and defines b in terms of a.

By restricting a to [0,1], and defining b as 1 - a, we  create a balanced tradeoff. Under this restriction and 
definition, a + b always equals 1. This actually fixes a loto of problems - when a + b doesn't equal 1, the fractal 
produced is larger or smaller than you would expect, which causes problems for rendering them.

Once a is on the interval [0,1] and b = 1-a, by increasing and decreasing the value of a by specified amounts, smooth 
transformations of the set become possible. All one has to do is set a = x/y, where x is how much of the fractal a is 
linked to, and y is how many intervals you want in the transformation, minus one. If you want a two step transformation,
y should equal 1, since that gives two in-range values for x - 0 and 1.

This lets you interpolate between two fractals linearly!

Fractale basically automates this process, and allows any term to be interpolated in any way, at any time.

In addtion to this linear method, fractale also supports a sinusoidal method, which takes advantage of the fact that 
sin(x)^2 + 1-sin(x)^2 = 1. The sinusoidal method has a slow start, quick middle, and slow finish.

The linear method had constant speed throughout.

Other methods are being considered; most especially ones that feature dynamic speed adjustment based on what you are 
doing to the terms to make transformations that don't proceed linearly, do so. For example, if you move from a z^2 
mandelbrot to z^6, you will notice that most of the animation is spent in a "mostly z^6-ish shape" increase the 
difference between powers, and eventually, you reach a stage where every fram of the animation seems to be nothing but 
the higher power version, except for the first.

## Animating New Terms

Let's say you wish to go from z + c to z + c + p. Unlike an interpolation from z to p, or from z + z to p + z, you can't
get there just by changing what you already have, since you're moving from 2 to 3 terms.

You can always give the renderer z + c + 0 as your starting formula, and interpolate 0 with p. But Fractale also allows 
you to easily add a new term to the animation if you have a new idea. To do this, simply call addTerm(node). If you want
to add a term to the top level, node can be any top level adress. If you want it to be a subterm of a term, node can be 
the address of any subterm.

The code *always* add your new term to the *end* of the list of terms (it will be the last term in that part of the 
formula). Because of this, as a best practice, it is reccomended that you use term 0 for top level, and a blank subterm
for deeper levels. Other uses will work, but it will make it harder for humans to understand your animations.

Ex:

addTerm("0") = Add a term to the top level.
addTerm("0.") = Add a subterm to term 0.
addterm("1.3.") = Add a subterm to subterm 3 of term 1.

# Raw Output
Because Supersets are largely non-optimisable with traditional techniques, and because I didn't feel like brainstorming
new and improved algorithms, Fractale supports saving raw output. The benefit of saving raw output as opposed to
rendering directly is that a raw-output file saves the total results of a calculation prior to colouring.

*Colouring is the least expensive step in terms of compute time.* Thus, by saving the results of one calculation to raw
output, you can rapidly try as many different colouring methods as you like one the file; without having to wait.
Furthermore, if Fractale is ever updated with new features, then you can use the raw output with those new features.
Every effort has been taken to ensure that Fractale's raw output represents a complete record of all data calculation
produces.

Finally, though not availile now, an eventual feature is planned for raw output such that you can use a raw output file
to bootstrap a larger render in the same numerical range as the previous file, saving compute time.

## The .mfield File Format
It's a giant, ugly, uncompressed raw list for now. Sorry.

ef that, make it a binary file at least...


## License
License is WTFPL 2.0, because really, who would?