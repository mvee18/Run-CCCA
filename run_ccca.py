import math
import os
import subprocess
import numpy

# Remember that "final" is the geometry array that you want.
# Order of methods/basis + mem needed:
#
# aug-cc-pVDZ 195 mw
# aug-cc-pVTZ 995 mw
# aug-cc-pVQZ 1995 mw
# CCSD(T)/cc-pVTZ	195 mw
# MP2/cc-pVTZ	995 mw
# MP2(FC1)/aug-cc-pCVTZ 995 mw
# MP2-DK/cc-pVTZ-DK 195 mw

dirs = ["dz","tz","qz","ccsdt","ccpvtz","fc1","dk"]
basis_sets = ['aug-cc-pVDZ','aug-cc-pVTZ','aug-cc-pVQZ','cc-pVTZ','cc-pVTZ','aug-cc-pCVTZ','cc-pVTZ-DK']
walltime = ['08:00:00', '72:00:00', '168:00:00', '168:00:00','8:00:00','168:00:00','48:00:00']
memorygb = [2,8,32,2,16,8,2]
memory_list = [195,495,1995,195,995,495,195]
# Extract geomtry data:


#This will print the header and geometry.
for count,i in enumerate(dirs):
    os.chdir("/home/mvee/Desktop/Python/b3lyp")
    temp = open('tmp.txt', 'r')
    os.chdir("/home/mvee/Desktop/Python/")
    # This will create directories if they do not exist.
    if not os.path.exists(dirs[count]):
        os.mkdir(dirs[count])
        print("Directory Created ")
    else:
        print("Directory already exists")
    os.chdir("/home/mvee/Desktop/Python/%s" %(dirs[count]))
    print(os.getcwd())
    f = open('input.com', 'w+')
    f.write("memory,%d,m\n" %memory_list[count])
    f.write("\nnocompress;\n")
    f.write("geomtyp=xyz\n")
    f.write("angstrom\n")
    f.write("geometry={\n")
    f.write(temp.read())
    f.write("}")
    f.write("\n")
f.close()
temp.close()

# Time to create the footer:
# We will use the same type of for loop above, however, using 'a' to see if it goes wrong somewhere here.
# We also have no more use for the temp file.

for count,i in enumerate(dirs):
    os.chdir("/home/mvee/Desktop/Python/%s" %(dirs[count]))
    f = open('input.com', 'a')
    f.write("\nbasis=%s;\n" %(basis_sets[count]))
    print(count)
    if count <= 2:
        f.write("set,charge=0\n")
        f.write("set,spin=0\n")
        f.write("hf\n")
        f.write("mp2")
    elif count == 3:
        f.write("set,charge=0\n")
        f.write("set,spin=0\n")
        f.write("hf\n")
        f.write("{CCSD(T)}")
    elif count == 4:
        f.write("set,charge=0\n")
        f.write("set,spin=0\n")
        f.write("hf\n")
        f.write("mp2")
    elif count == 5:
        f.write("set,charge=0\n")
        f.write("set,spin=0\n")
        f.write("hf\n")
        f.write("{mp2;core}")
    elif count == 6:
        f.write("dkroll=1;\n")
        f.write("set,charge=0\n")
        f.write("set,spin=0\n")
        f.write("hf\n")
        f.write("mp2")

# Now, the PBS Files.
for count,i in enumerate(dirs):
    os.chdir("/home/mvee/Desktop/Python/%s" %(dirs[count]))
    f = open('input.pbs', 'w+')
    f.write("#!/bin/sh\n")
    f.write("#PBS -N %s\n" %(dirs[count]))
    f.write("#PBS -S /bin/bash\n")
    f.write("#PBS -j oe\n")
    f.write("#PBS -W umask=022\n")
    f.write("#PBS -l walltime=%s\n" %(walltime[count]))
    if count == 6:
        f.write("#PBS -l ncpus=1\n")
    else:
        f.write("#PBS -l ncpus=2\n")
    f.write("#PBS -l mem=%dgb\n\n" %(memorygb[count]))
    f.write("module load intel\n")
    f.write("module load mpt\n")
    f.write("export PATH=/ptmp/bwhopkin/molpro_mpt/2012/molprop_2012_1_Linux_x86_64_i8/bin:$PATH\n\n")

    f.write("export WORKDIR=$PBS_O_WORKDIR\n")
    f.write("export TMPDIR=/tmp/$USER/$PBS_JOBID\n")
    f.write("cd $WORKDIR\n")
    f.write("mkdir -p $TMPDIR\n\n")

    f.write("date")
    f.write("mpiexec molpro.exe input.com\n")
    f.write("date\n\n")

    f.write("rm -rf $TMPDIR")
