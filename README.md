# CCCA Method for Molpro
### Introduction
This script will generate the files required to run a CCCA (Correlation Consistent Composite Approach) in Molpro, given an optimized B3LYP output file. 

### Usage
Run the `run_ccca.py` script in the folder which contains the b3lyp.out file, this will generate a tmp.txt file containing the optimized geometry from the B3LYP output and the folders necessary for the CCCA method.

**Note:** The script generates the folders in the directory above, so if, for example, the path to the b3lyp.out is `/path/to/b3lyp_out/b3lyp.out`, then the folders will be generated in the `/path/to/b3lyp_out/` directory.

The following directories will be generated:
"dz","tz","qz","ccsdt","ccpvtz","fc1","dk", which correspond to the following methods/basis sets.

- MP2/aug-cc-pVDZ
- MP2/aug-cc-pVTZ
- MP2/aug-cc-pVQZ
- CCSD(T)/cc-pVTZ
- MP2/cc-pVTZ
- MP2(FC1)/aug-cc-pCVTZ
- MP2-DK/cc-pVTZ-DK (Douglass-Kroll Hess Hamiltonian)

These will contain an input.pbs and an input.com file. You may have to change the pbs file depending on your supercomputer's architecture. 

### Known Issues
The script will only correctly convert the elements H, C, O, Mg, Al, Si, Ca, though a very easy addition at line 38 in the format:
<pre>
if value == '#':
    geom[i][j] = 'X'
</pre>
where # is the atomic number of the element and X is the symbol (leaving the parentheses). 

### Additional Resources
https://en.wikipedia.org/wiki/Quantum_chemistry_composite_methods#Correlation_consistent_composite_approach_(ccCA)
