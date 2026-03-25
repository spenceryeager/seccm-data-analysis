# Quartile KappaNaught and Alpha Values

This is from the Oldham-Zoski paper on using quartiles to determine the kinetics of a sigmoid voltammogram. These three separate files are calculated from oldham_zoski_quartiles.py, and can be loaded & cross referenced to find a kinetics values. I'm leaving the option to increase the resolution of the calculations by changing the intervals of alpha & kappa naught. 

BIG NOTE: When using these values, the transfer coefficient (symmetry of reaction) is displayed as is. KappaNaught, however, is NOT THE FINAL RATE COEFFICIENT VALUE!

This is a dimensionless factor that combines different geometric factors & the standard rate coefficient. Its definition is...

kappanaught = pi * k0 * a / (4 Do) where Do is the diffusion coeffiicent and a is the radius of the UME.
