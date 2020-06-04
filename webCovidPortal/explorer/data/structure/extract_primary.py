import numpy as np, pandas as pd;
import os,sys;
################################################################################
source_folder = "./downloads";
chain_file = "./chains.csv";
outfile = "./atoms.csv";
################################################################################
# get chains
use_chains = ['S PROTEIN','SPIKE GLYCOPROTEIN'];
use_atoms = ['CA'];
# get the first chain that matches from each PDB
chains = pd.read_csv(chain_file);
chains = chains[chains['mol_name'].isin(use_chains)];
# chains = chains.drop_duplicates(subset=['pdb_id','mol_name'], keep='first');
atoms = [];
# parse atoms
for pdb_id in chains['pdb_id'].unique():
    ss = chains[chains['pdb_id']==pdb_id];
    unique_chains = list(ss['chain'].unique());
    # expect at least one chain
    if len(ss)<1:
        raise Exception("No chains for PDB ID "+str(pdb_id));
    # open file and read
    fn = str(pdb_id)+".pdb";
    fh = open(source_folder+"/"+fn,'r');
    lines = fh.readlines();
    fh.close();
    print(str(pdb_id)+"...");
    # parse atoms
    for l in lines:
        if (l[0:4]=="ATOM") and (l[21] in unique_chains):
            if l[12:16].replace(' ','') in use_atoms:
                spec = {
                    'pdb'       : pdb_id,
                    'atom'      : l[12:16].replace(' ',''),
                    'resname'   : l[17:20].replace(' ',''),
                    'chain'     : l[21].replace(' ',''),
                    'resid'     : l[22:26],
                    'icode'     : l[26].replace(' ',''),
                    'element'   : l[76:78].replace(' ',''),
                    'charge'    : l[78:80].replace(' ',''),
                    'occupancy' : l[54:60].replace(' ',''),
                    'x'         : l[30:38],
                    'y'         : l[38:46],
                    'z'         : l[46:54],
                };
                atoms.append(spec);

# format
atoms = pd.DataFrame(atoms);
atoms['resid'] = atoms['resid'].astype(int);
atoms['x'] = atoms['x'].astype(float);
atoms['y'] = atoms['y'].astype(float);
atoms['z'] = atoms['z'].astype(float);
atoms['charge'] = atoms['charge'].replace('',0).astype(int);
atoms['occupancy'] = atoms['occupancy'].replace('',0).astype(float);
# write
print("Writing to "+outfile);
atoms.to_csv(outfile);


# fin.
