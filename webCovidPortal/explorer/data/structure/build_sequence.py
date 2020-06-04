import numpy as np, pandas as pd;
import os, sys;
################################################################################
atom_file = "./atoms.csv";
outfile = "./sequences.csv";
################################################################################
atoms = pd.read_csv(atom_file);
groupkey = "_pdb_chain";
atoms['resid'] = atoms['resid'].astype(int); # enforce for sorting
atoms[groupkey] = atoms['pdb'] + "_" + atoms['chain'];
################################################################################
## AA lookup table
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
aa_t2s = dict(zip(aa['triplet'], aa['letter']));
################################################################################
sequences = [];
for group in atoms[groupkey].unique():
    print(str(group)+"...");
    # subset
    ss = atoms[atoms[groupkey]==group].sort_values(by='resid');
    seq = ''.join([ aa_t2s[t] for t in ss['resname'] ]);
    pos = ','.join(ss['resid'].astype(str));
    sequences.append({
        'pdb'       : ss.iloc[0]['pdb'],
        'chain'     : ss.iloc[0]['chain'],
        'sequence'  : seq,
        'position'  : pos,
    });
sequences = pd.DataFrame(sequences);
print("Writing "+outfile);
sequences.to_csv(outfile);
