import numpy as np, pandas as pd;
import sys;
################################################################################
preconformed_alignment_file = "./preconformed_alignments.csv";
conformed_sequences_file = "./db_taxon_sequences.csv";
outfile = "./conformed_alignments.csv";
################################################################################
preconformed_seqs = pd.read_csv(preconformed_alignment_file);
conformed_seqs = pd.read_csv(conformed_sequences_file);
################################################################################
# give PDB sequences an accession number
for ix in preconformed_seqs[preconformed_seqs['accession'].isnull()].index:
    preconformed_seqs.loc[ix,'accession'] = \
        "PDB."+ \
        str(preconformed_seqs.loc[ix,'pdb']) + ":"+ \
        str(preconformed_seqs.loc[ix,'chain']);
################################################################################
# Conforms sequences from one alignment (preconformed) to another (conformed)
# by pivoting on a reference sequence that is present in both alignments.
#
# This particular script is made to conform local alignments of PDB sequences
# with related sequences based taxon id's (preconformed, taxon alignment) to a
# universal alignment of betacoronaviruses (conformed) used for the explorer
# sequences.
#
# Conformation requires at least one preconformed sequence to satisfy:
#   1. A conformed version of the same sequence must exist.
#   2. The pre-conformed version cannot have gaps ('-').
#
# The reference is chosen as the first preconformed sequence that is not a
# PDB sequence and has no gaps. If no preconformed reference can be found the
# entries for that taxon alignment are all ignored.
#
# Conformation is done by inserting gaps from the conformed reference sequence
# into the same positions in the preconformed taxon alignment sequences.
# Finally, the newly conformed reference (from the preconformed sequences) is
# checked against the original conformed reference to ensure gaps were inserted
# properly.
#
final_seqs = []; # final conformed sequences
for taxon_id in preconformed_seqs['taxon_id'].unique():
    print(str(taxon_id)+" .. ", end='', flush=True);
    if taxon_id not in conformed_seqs['taxon_id'].values:
        print("Taxon not found in conformed references.");
        continue;
    pc_ss = preconformed_seqs[preconformed_seqs['taxon_id']==taxon_id];
    c_ss = conformed_seqs[conformed_seqs['taxon_id']==taxon_id];
    # get references (which are in both sets)
    ref_match = pc_ss['accession'].isin(c_ss['accession']);
    pc_refs = pc_ss.loc[ ref_match[ref_match==True].index ];
    # select reference: first one that has no gaps
    pc_ref = [];
    for i,r in pc_refs.iterrows():
        if '-' not in r['sequence']:
            pc_ref = r;
    if len(pc_ref)<1:
        print("no valid preconformed reference found");
        continue;
    # isolate reference in conformed sequences
    c_ref = c_ss[c_ss['accession']==pc_ref['accession']].iloc[0];
    if len(c_ref)<1:
        print("reference doesn't exist in conformed sequences");
        continue;
    # conform old sequences to new
    c_ix = 0;
    pc_ix = 0;
    # limit to reference and PDBs only
    pc_ss = pc_ss[
        (pc_ss['pdb'].notnull()) |
        (pc_ss['accession']==c_ref['accession'])
    ];
    # initialize conformed strings
    conformed = {};
    for acc in pc_ss['accession']:
        conformed[acc] = {
            'sequence': "",
            'offset': c_ref['offset'],
            'accession': acc,
            'alignment': c_ref['alignment'],
        };
    # conform
    for c_ix in range(0,len(c_ref['sequence'])):
        # if c_ref is a gap then store a gap, otherwise store residues
        if c_ref['sequence'][c_ix]=='-':
            for i,r in pc_ss.iterrows():
                conformed[r['accession']]['sequence'] += '-';
            # don't increment preconformed position until no gaps in conformed
        else:
            for i,r in pc_ss.iterrows():
                conformed[r['accession']]['sequence'] += r['sequence'][pc_ix];
            pc_ix+=1; # and move to next preconformed position
    # confirm match between references
    if conformed[c_ref['accession']]['sequence']!=c_ref['sequence']:
        # give a nice diagonostic if they don't match...
        print("Conformed alignment doesn't match reference:");
        print(c_ref['sequence']);
        print();
        print(conformed[c_ref['accession']]['sequence']);
        print();
        print();
        print();
        continue;
    final_seqs += list(conformed.values());
    print("OK");
final_seqs = pd.DataFrame(final_seqs);
print("Writing "+outfile);
final_seqs.to_csv(outfile);

# fin.
