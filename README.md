# fractale

Fractale is a fractal fractal calculator calculator designed by me for the sole putpose of doing things other calculators won't let me do without paying for them. The main use case is the creation of so-called fractal supersets, which are awesome images made by compressing julia sets into pixels to create maps of juliaspace. 

I don't particularly care about how nice looking the codebase is, so prepare for your eyes to bleed on the sheer amateur-hour-ness of it.


##License
License is WTFPL 2.0, because really, who would?


##TODO
* Rewrite toPPX() function so pixels can be streamed to it, thus reducing memory use
* rewrite rendering architecture so that z is a vector of all of z's states thus allowing more colouring algos + implicit storage of c as z[0]
* create colourspace.py class for HSL-HSV-RGB-WHATEVER colour conversions.
* rewrite fractale.py architecture to be less pants-on-head stupid
