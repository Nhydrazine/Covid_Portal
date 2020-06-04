import numpy as np, pandas as pd;
import re, sys;
################################################################################
infile = "clustalo-E20200519-140102-0914-92371964-p1m.clustal_num";
outfile = "aligned.csv";
################################################################################
def loadClustal(fh):
    """Loads clustal-formatted sequences from a file handle.

    Parameters
    ----------
    fh : file_object
    File handle to read sequences from.

    Returns
    -------
    pandas.Series
    Series of sequences as individual strings, indexed by sequence ID/name.

    Examples
    --------
    >>> with open('SEQUENCES.clustal','r') as fh:
    >>> 	seqs = loadClustal(fh);
    >>> print(seqs);

    """
    seqs = {};
    defined = [];
    rx = re.compile('^([^\s]+?)\s+([^\s]+?)\s+\d+$');
    for l in fh.read().split('\n')[1:]:
        if len(l)>0:
            m = re.match(rx,l);
            if not m:
                continue;
            seqid = m.group(1);
            seq = m.group(2);
            if (seqid in seqs.keys()):
                seqs[seqid] += str(seq);
            else:
                seqs[seqid] = seq;
                defined.append(seqid);
    return pd.Series(seqs, dtype=str);
################################################################################

with open(infile,'r') as fh:
    seqs = loadClustal(fh);
df = pd.DataFrame({
    'accession': seqs.index.to_list(),
    'sequence': seqs
});
df.to_csv(outfile, index=False);





# fin
