import numpy as np, pandas as pd;
import os,sys;
################################################################################
source_folder = "./downloads";
infile = "./chains.csv";
outfile_sheets = "./sheets.csv";
outfile_helices = "./helices.csv";
outfile_seqreses = "./seqreses.csv";
################################################################################
# get chains
use_chains = ['S PROTEIN','SPIKE GLYCOPROTEIN'];
# get the first chain that matches from each PDB
chains = pd.read_csv(infile);
chains = chains[chains['mol_name'].isin(use_chains)];
# chains = chains.drop_duplicates(subset=['pdb_id','mol_name'], keep='first');

sheets = [];
helices = [];
seqreses = [];

aa = pd.DataFrame([
"G GLYCINE GLY".split(" "),
"A ALANINE ALA".split(" "),
"L LEUCINE LEU".split(" "),
"M METHIONINE MET".split(" "),
"F PHENYLALANINE PHE".split(" "),
"W TRYPTOPHAN TRP".split(" "),
"K LYSINE LYS".split(" "),
"Q GLUTAMINE GLN".split(" "),
"E GLUTAMATE GLU".split(" "),
"S SERINE SER".split(" "),
"P PROLINE PRO".split(" "),
"V VALINE VAL".split(" "),
"I ISOLEUCINE ILE".split(" "),
"C CYSTEINE CYS".split(" "),
"Y TYROSINE TYR".split(" "),
"H HISTIDINE HIS".split(" "),
"R ARGININE ARG".split(" "),
"N ASPARAGINE ASN".split(" "),
"D ARPARTATE ASP".split(" "),
"T THREONINE THR".split(" "),
], columns=["letter","name","triplet"]);

for pdb_id in chains['pdb_id'].unique():
    ss = chains[chains['pdb_id']==pdb_id];
    unique_chains = list(ss['chain'].unique());
    # expect at least one chain
    if len(ss)<0:
        raise Exception("No chains for PDB ID "+str(pdb_id));
    # open file and read
    fn = str(pdb_id)+".pdb";
    fh = open(source_folder+"/"+fn,'r');
    lines = fh.readlines();
    fh.close();
    # parse
    for l in lines:
        if l[0:5]=="SHEET":
            if (l[21] in unique_chains) and (l[32] in unique_chains):
                spec = {
                    'pdb'           : pdb_id,
                    'sheet'         : l[11:14],
                    'strand'        : int(l[7:10].replace(' ','')),
                    'start_chain'   : l[21].replace(' ',''),
                    'end_chain'     : l[32].replace(' ',''),
                    'start_resname' : l[17:20].replace(' ',''),
                    'end_resname'   : l[28:31].replace(' ',''),
                    'start_resid'   : int(l[22:26].replace(' ','')),
                    'end_resid'     : int(l[33:37].replace(' ','')),
                };
                sheets.append(spec);
        elif l[0:5]=="HELIX":
            if (l[19] in unique_chains) and (l[32] in unique_chains):
                spec = {
                    'pdb'           : pdb_id,
                    'helix'         : l[11:14].replace(' ',''),
                    'serial'        : int(l[7:10].replace(' ','')),
                    'start_chain'   : l[19].replace(' ',''),
                    'end_chain'     : l[31].replace(' ',''),
                    'start_resname' : l[15:18].replace(' ',''),
                    'end_resname'   : l[27:30].replace(' ',''),
                    'start_resid'   : int(l[21:25].replace(' ','')),
                    'end_resid'     : int(l[33:37].replace(' ','')),
                };
                helices.append(spec);
        elif l[0:6]=="SEQRES":
            if l[11] in unique_chains:
                spec = {
                    'pdb'           : pdb_id,
                    'chain'         : l[11],
                    'serial'        : int(l[7:10].replace(' ','')),
                    'residues'      : l[19:].rstrip(),
                };
                seqreses.append(spec);

sheets = pd.DataFrame(sheets);
print("Writing "+outfile_sheets);
sheets.to_csv(outfile_sheets);
helices = pd.DataFrame(helices);
print("Writing "+outfile_helices);
helices.to_csv(outfile_helices);
seqreses = pd.DataFrame(seqreses);
print("Writing "+outfile_seqreses);
seqreses.to_csv(outfile_seqreses);

# fin.
