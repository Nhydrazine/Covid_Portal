import numpy as np, pandas as pd;
################################################################################
chains_file = "../chains.csv";
outfile = "select_taxa_seqs.sql";
################################################################################
chains = pd.read_csv(chains_file);
chains = chains.drop_duplicates(subset=['pdb_id','mol_name'], keep='first');
# get distinct taxon IDs
taxa = chains['taxon_id'].astype(str).unique();
# generate select SQL
SQL = """
select
    t.gb_taxon_id as taxon_id,
    t.name,
    t.leaf,
    sr.organism,
    sr.isolate,
    sr.accession,
    aln.name as alignment,
    s.sequence,
    s.offset
from explorer_taxon as t
join explorer_sequencerecord as sr on sr.taxon_id==t.id
join explorer_sequence as s on s.sequence_record_id=sr.id
join explorer_alignment as aln on aln.id = s.alignment_id
where t.gb_taxon_id in ("""+','.join(taxa)+""")
and explorer_alignment.name = "20200505"
""";
with open(outfile,'w') as fh:
    fh.write(SQL);
