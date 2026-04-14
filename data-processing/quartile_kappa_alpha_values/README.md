# Quartile KappaNaught and Alpha Values

## OLD! Not needed to be used anymore

These values came from an analytical expression used to make solving the current-potential Butler-Volmer relationship for UMEs easier. A product of it's time, these days the current-potential relationship can be easily modeled in Python and the kinetics parameters can be extracted quite simply. I wasted a non-marginal amount of time writing out and implementing this method, only to be use my original voltammogram simulator in the end! But, it helped me realize that I had to redefine some of the parameters for an oxidation process as opposed to a reduction process, an important realization.

*The new values that should be used are in **sigmoid_simulation_values**, which is a much more complete list of values.

## Original Description

This is from the Oldham-Zoski paper on using quartiles to determine the kinetics of a sigmoid voltammogram. These three separate files are calculated from oldham_zoski_quartiles.py, and can be loaded & cross referenced to find a kinetics values. I'm leaving the option to increase the resolution of the calculations by changing the intervals of alpha & kappa naught. 

BIG NOTE: When using these values, the transfer coefficient (symmetry of reaction) is displayed as is. KappaNaught, however, is NOT THE FINAL RATE COEFFICIENT VALUE!

This is a dimensionless factor that combines different geometric factors & the standard rate coefficient. Its definition is...

kappanaught = pi * k0 * a / (4 Do) where Do is the diffusion coeffiicent and a is the radius of the UME.
