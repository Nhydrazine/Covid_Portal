import numpy as np, pandas as pd;
import re;
################################################################################
chain_file = "./chains.csv";
sequence_file = "./alignment/conformed_alignments.csv";
atom_file = "./atoms.csv";
################################################################################
structurechain_file = "./imports/structureChains.csv";
structuresequence_file = "./imports/structureSequences.csv";
structureatom_file = "./imports/structureAtoms.csv";
################################################################################
# Structures and Chains
################################################################################
# for merged/deprecated taxon IDs
taxon_replace = {
    "227859"    : "694009"
};
df = pd.read_csv(chain_file);
df['taxon_id'] = df['taxon_id'].astype(str).replace(to_replace=taxon_replace);
hard_coded_mesh = "D064370"; # coronavirus spike protein
df['protein'] = hard_coded_mesh;
columns = ['pdb_id','taxon_id','protein','chain'];
print("Loaded "+str(len(df))+" PDB chains");
print("Writing "+structurechain_file);
df[columns].to_csv(structurechain_file);
################################################################################
# Structure Sequences
################################################################################
rx_structurename = re.compile('^PDB\.(.*?)\:(.)$');
rx_leadinggaps = re.compile('^(\-*)(.*)$');
df = pd.read_csv(sequence_file);
# get PDB id and chain from pdb-style accession
df = pd.concat([
    df,
    df['accession'].str.extract(
        rx_structurename
    ).rename(columns={0:'pdb_id', 1:'chain'})
], axis=1);
# drop all records that don't match the pdb-style accession
df = df[df['pdb_id'].notnull()];
# trim leading gaps and adjust offset
trims = df['sequence'].str.extract(rx_leadinggaps);
df['_add_offset'] = [ len(l) for l in trims[0].astype(str) ];
df['offset'] = df['offset'].astype(int) + df['_add_offset'];
df['sequence'] = trims[1];
columns = ['pdb_id','chain','alignment','offset','sequence'];
print("Writing "+structuresequence_file);
df[columns].to_csv(structuresequence_file);
################################################################################
# Sequence Atoms
################################################################################
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
df = pd.read_csv(atom_file);
df['pdb_id'] = df['pdb'];
# build resix
df['resix'] = np.nan;
df['_group'] = df['pdb_id']+'_'+df['chain'];
for g in df['_group'].unique():
    ss_ix = df[df['_group']==g]['resid'].sort_values().index;
    df.loc[ss_ix,'resix'] = np.arange(0,len(ss_ix));
df['resix'] = df['resix'].astype(int);
# build resn
t2l = dict(zip(aa['triplet'], aa['letter']));
df['resn'] = [ t2l[t] for t in df['resname'] ];
df['resn'] = df['resn'].fillna('X');
columns = [
    'pdb_id',
    'chain',
    'resix',
    'resid',
    'resn',
    'atom',
    'element',
    'charge',
    'occupancy',
    'x',
    'y',
    'z',
];
print("Writing to "+structureatom_file);
df[columns].to_csv(structureatom_file);

# fin.
