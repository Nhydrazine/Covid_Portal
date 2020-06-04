import numpy as np, pandas as pd;
################################################################################
filename = "VIPR-EXPORT-20200516";
infile = filename+"-EXPANDED.csv";
synfile = filename+"-PNAMES-MARKED.csv";
outfile = filename+"-EXPANDED-RESTRICTED.csv";
################################################################################
print("Loading synonyms from "+synfile);
syns = pd.read_csv(synfile);
syns = syns[syns['Spike Synonym']==1];
syns = syns['Protein Names'].to_list();

print("Loading entries from "+infile);
df = pd.read_csv(infile);
df['_tag'] = 0;

original_size = len(df);
print("Restricting "+str(original_size)+" entries...");
for i,r in df.iterrows():
    pnames = r['Protein Names'].split(',');
    tag = False;
    for p in pnames:
        if p in syns:
            tag = True;
            break;
    if tag==True:
        df.loc[i,'_tag']=1;
        continue;

restricted = df[df['_tag']==1].copy();
# convert to MeSH term
restricted['Protein Names'] = "Spike Glycoprotein, Coronavirus";
print("Have "+str(len(restricted))+" entries remaining.");
print("Writing "+outfile);
restricted[df.columns].to_csv(outfile);
