import numpy as np, pandas as pd;
import re, sys;
################################################################################
infile = "clustalo-E20200519-140102-0914-92371964-p1m.clustal_num";
outfile = "aligned.fasta";
################################################################################
def formatFASTA(seqs, sequence_split_length=80):
    """Converts a pandas.Series of sequence strings into FASTA format for output.

    Parameters
    ----------
    seqs : pandas.Series
    A series of sequence strings indexed by ID/name.
    sequence_split_length : int
    Character length of a single line of sequence in FASTA output file.

    Returns
    -------
    str
    FASTA-formatted sequence output.

    """
    buff = [];
    for i in seqs.index:
        buff.append(">" + str(i));
        buff += [
            seqs[i][p:p+sequence_split_length] for p in range(0,len(seqs[i]),sequence_split_length)
        ];
    return '\n'.join(buff);
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
with open(outfile,'w') as fh:
    fh.write(formatFASTA(seqs));




# fin
