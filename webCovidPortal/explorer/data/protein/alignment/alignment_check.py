import numpy as np, pandas as pd;
################################################################################
infile = "20200518_clustalo.aln";
outfile = "aligned_accessions.csv";
################################################################################
accessions = [];
fh = open(infile,'r');
sequence_limit = 2000;
# skip first three lines
for i in range(0,3):
    fh.readline();

for i in range(0,sequence_limit):
    l = fh.readline();
    if l.strip() == "":
        break;
    else:
        accessions.append(l[0:20].replace(' ',''));
fh.close();
print(accessions);
