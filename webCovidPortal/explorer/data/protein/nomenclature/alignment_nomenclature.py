import numpy as np, pandas as pd;
################################################################################
infile = "../alignment/aligned.fasta";
reference_accession = "Q14EB0.1";
nomenclature_name = "SARS Spike HKU1-N2";
alignment_name = "20200505";
protein_mesh_id = "D064370";
outfile = reference_accession+"-nomenclature.csv";
################################################################################
def loadFASTA(fh):
    """Load sequences from a FASTA file.

    Parameters
    ----------
    fh : file_object

    Returns
    -------
    pandas.Series
        A series of sequence strings indexed by ID/name

    Examples
    --------
    Minimal working example.
    >>> import numpy as np, pandas as pd;
    >>> import simpleSeq.IO as ssio;
    >>> with open('SEQUENCES.fasta','r') as fh:
    >>>     seqs = ssio.loadFASTA(fh);
    >>> print(seqs);

    """
    seqs = {};
    current = "";
    for l in fh.read().split('\n'):
        if l[0]=='>': current = l[1:];
        else:
            if current in seqs.keys():
                seqs[current] += str(l);
            else:
                seqs[current] = str(l);
    return pd.Series(seqs, dtype=str);
################################################################################
max_subdigits = 3;
with open(infile,'r') as fh:
    seqs = loadFASTA(fh);
major = [];
minor = [];
pos = 0;
subpos = 0;
for c in seqs[reference_accession]:
    if c=='-':
        subpos += 1;
    else:
        subpos=0;
        pos+=1;
    major.append(str(pos));
    minor.append(str(subpos).rjust(max_subdigits,'0'));
pnom = pd.DataFrame({
    'major': major,
    'minor': minor
});
pnom['protein'] = protein_mesh_id;
pnom['reference'] = reference_accession;
pnom['alignment_name'] = alignment_name;
pnom['name'] = nomenclature_name;
pnom.to_csv(outfile);



#print(seqs);
