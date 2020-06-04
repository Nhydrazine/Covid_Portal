import sys;
import numpy as np, pandas as pd;
################################################################################
infile = "gb_extract.csv";
outfile = "gb_foralignment_byaccession.fasta";
################################################################################
print("Loading "+infile);
df = pd.read_csv(infile);
fasta = [];
print("Converting "+infile);
lw = 80; # sequence line width in characters
for i,r in df.iterrows():
    name = r['version'];
    seq = r['seq'];
    if len(seq)<500: continue; # skip short sequences
    fasta.append(">"+name);
    fasta = fasta + [ seq[i:i+(lw-1)] for i in range(0, len(seq), (lw-1)) ];
print("Writing "+outfile);
with open(outfile, 'w') as fh:
    fh.write("\n".join(fasta));
print("Done.");
