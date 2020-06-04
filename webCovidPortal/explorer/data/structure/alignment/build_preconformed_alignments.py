import numpy as np, pandas as pd;
import re;
################################################################################
alignment_files = [
'aligned/aligned_228407.aln',
'aligned/aligned_1235996.aln',
'aligned/aligned_1263720.aln',
'aligned/aligned_2697049.aln',
'aligned/aligned_443239.aln', # <-- this one has inserts in accession
];
outfile = "preconformed_alignments.csv";
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
rx_parse_accession = re.compile('^ACCESSION\=(.+?)\;CHAIN\=X\;TAXID\=(.+)$');
rx_parse_pdb = re.compile('^PDB\=(.+?)\;CHAIN\=(.+?)\;TAXID\=(.+)$');

preconform_sequences = [];
for fn in alignment_files:
    print(fn);
    with open(fn,'r') as fh:
        local_aligned_seqs = loadClustal(fh);
    # parse names
    for ix in local_aligned_seqs.index.astype(str):
        m = re.match(rx_parse_accession, ix);
        if m:
            preconform_sequences.append({
                'accession'     :   m.group(1),
                'pdb'           :   "",
                'chain'         :   "",
                'taxon_id'      :   m.group(2),
                'sequence'      :   local_aligned_seqs[ix],
            });
            continue;
        m = re.match(rx_parse_pdb, ix);
        if m:
            preconform_sequences.append({
                'accession'     :   "",
                'pdb'           :   m.group(1),
                'chain'         :   m.group(2),
                'taxon_id'      :   m.group(3),
                'sequence'      :   local_aligned_seqs[ix],
            });
            continue;
preconform_sequences = pd.DataFrame(preconform_sequences);
print("Writing "+outfile);
preconform_sequences.to_csv(outfile);


# fin.
