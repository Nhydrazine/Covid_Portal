import numpy as np, pandas as pd;
################################################################################
filename = "VIPR-EXPORT-20200516";
infile = filename + ".csv";
outfile = filename + "-PNAMES.csv";
################################################################################
print("Loading "+infile);
df = pd.read_csv(infile);
pnames = [];
print("Extracting Protein Names...");
for i,r in df.iterrows():
    pnames += r['Protein Names'].split(',');
pnames = pd.Series(pnames);
unique_pnames = pd.DataFrame({'Protein Names': pnames.unique()});
print("Writing "+outfile);
unique_pnames.to_csv(outfile);
