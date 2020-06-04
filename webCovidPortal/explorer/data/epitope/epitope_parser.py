import sys;
import numpy as np, pandas as pd;
####################################################################
filename = "VIPR-EXPORT-20200516";
infile = filename + ".csv";
outfile = filename + "-EXPANDED.csv";
####################################################################
print("Loading "+infile);
df = pd.read_csv(infile);
# list of columns that are comma joined in VIPR export
splitcols = [
    'Host',
    'Assay Type Category',
    'Assay Result',
    'MHC Allele Name',
    'MHC Allele Class',
    'Method',
    'Measurement',
];
# list of columns that are replicated across expansion
repcols = [
    'IEDB ID',
    'Epitope Sequence',
    'Protein Names',
]
expanded = [];
print("Expanding...");
for i,r in df.iterrows():
    splits = { };
    mastercount = 0;
    # expand split colkumns and verify size
    for c in splitcols:
        splits[c] = r[c].split(',');
        if mastercount==0: mastercount = len(splits[c]);
        if len(splits[c]) != mastercount:
            raise ValueError("Invalid comma split item count for column "+c);
    # build expaned DF
    rows = pd.DataFrame(splits);
    # add replicated columns
    for c in repcols:
        rows[c] = r[c];
    expanded.append(rows);
expanded = pd.concat(expanded);
####################################################################
print("Writing to "+outfile);
expanded[df.columns].to_csv(outfile, index=True);
####################################################################
# fin.
