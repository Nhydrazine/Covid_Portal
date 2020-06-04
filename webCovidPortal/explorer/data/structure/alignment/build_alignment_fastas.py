import numpy as np, pandas as pd;
import sys;
################################################################################
chains_file = "../chains.csv";
pdb_sequence_file = "../sequences.csv";
taxon_sequence_file = "db_taxon_sequences.csv";
fasta_file_prefix = "prealign/fasta_prealign_";
################################################################################
chains = pd.read_csv(chains_file);
chains = chains.drop_duplicates(subset=['pdb_id','mol_name'], keep='first');
chains = chains.rename(columns={'pdb_id':'pdb'});
pdb_seqs = pd.read_csv(pdb_sequence_file);
pdb_seqs.index = pdb_seqs['pdb'];
chains.index = chains['pdb'];
pdb_seqs = pdb_seqs.join(chains, rsuffix="r");
taxa_seqs = pd.read_csv(taxon_sequence_file);
lw = 80; # line width in characters
for taxon in chains['taxon_id'].unique():
    db_seq_ss = taxa_seqs[taxa_seqs['taxon_id']==taxon];
    pdb_seq_ss = pdb_seqs[pdb_seqs['taxon_id']==taxon];
    if len(db_seq_ss)<=0:
        print("No DB sequences for taxon "+str(taxon)+", skipping");
        continue;
    else:
        print(str(len(db_seq_ss))+" DB sequences for taxon "+str(taxon)+".");
    if len(pdb_seq_ss)<=0:
        print("No PDB sequences for taxon "+str(taxon)+", skipping");
        continue;
    else:
        print(str(len(db_seq_ss))+" PDB sequences for taxon "+str(taxon)+".");

    # generate fasta file for sequences associated with this taxon
    fasta_file = fasta_file_prefix+str(taxon)+".fasta";
    buffer = [];
    for i,r in db_seq_ss.iterrows():
        name = str(
            "ACCESSION="+r['accession']+";"+
            "CHAIN=X;"+
            "TAXID="+str(r['taxon_id'])
        );
        buffer.append(">"+name);
        seq = r['sequence'].replace('-','');
        buffer = buffer + [
            seq[i:i+(lw-1)]
            for i in range(0, len(seq), (lw-1))
        ];
    for i,r in pdb_seq_ss.iterrows():
        name = str(
            "PDB="+r['pdb']+";"+
            "CHAIN="+r['chain']+";"+
            "TAXID="+str(r['taxon_id'])
        );
        buffer.append(">"+name);
        buffer = buffer + [
            r['sequence'][i:i+(lw-1)]
            for i in range(0, len(r['sequence']), (lw-1))
        ];

    print("Writing "+fasta_file);
    with open(fasta_file,'w') as fh:
        fh.write("\n".join(buffer));

# fin.
