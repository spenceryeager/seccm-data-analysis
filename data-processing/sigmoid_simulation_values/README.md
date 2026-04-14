# Sigmoid Simulation Values

These values come from simulating a voltammogram using the equations outlined in oldham_zoski_sim.py. Various various of kappa naught and alpha were chosen for simulation, along with their corresponding E1/2, E1/4, and E3/4 values. 

# Workflow for Analyzing SECCM Charge Transfer Voltammograms

Preanalysis note: oldham_zoski_sim.py is the primary code for simulating a singular voltammogram. oldham_zoski_batch_simulation.py simulates multiple voltammograms for different values of alpha & kappa naught, compiles it, and saves it into a directory.

1. bard_mirkin_batch_kinetics.py is used to extract the E1/4, E1/2, and E3/4 from experimental voltammograms. All voltammograms are processed using US Convention, such that anodic current is negative and cathodic current is positive. In the case of UME voltammograms, this means current normalization for a reduction event is 0 to 1, while current normalization for an oxidation event is 0 to -1.

2. quartile_processing.py is used to load in the simulated data and compare it to the extracted data, leading to a new file that contains the corresponding alpha and rate coefficient from the experimental data.

3. TBD. A program to compare the experimental voltammogram to the simulated parameters, resulting in a "goodness of fit" value that can be assigned to each voltammogram. 

Experimental voltammograms can have the same parameters extracted and matched to a corresponding alpha and kappanaught value. Tables for oxidation and reduction will be compiled to look through. 