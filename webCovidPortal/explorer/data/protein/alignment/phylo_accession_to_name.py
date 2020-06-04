import sys;
import numpy as np, pandas as pd;
################################################################################
# Newick formatted phylogentic tree file
phyfile = "clustalo-E20200519-140102-0914-92371964-p1m.ph.txt";
# csv containing "accession.version" as index and "organism" (e.g. name) columns
accnamefile = "../gbs_extract_step1.csv";
# output newick file
outfile = "named_phylogeny.tre";
################################################################################
# load accessions and names
df = pd.read_csv(accnamefile);
df = pd.DataFrame({
    'accession': df.iloc[:,0],
    'name': df['organism'].str.replace('[\s\,\(\)\.\[\]]','-', regex=True),
});
df['name'] = df['name'] + '-' + df['accession'];

# load phylo file
phylo = "";
with open(phyfile,'r') as fh:
    phylo = ''.join(fh.readlines());
# replace
for i,r in df.iterrows():
    phylo = phylo.replace(r['accession'], r['name']);
# write
with open(outfile,'w') as fh:
    fh.write(phylo);
