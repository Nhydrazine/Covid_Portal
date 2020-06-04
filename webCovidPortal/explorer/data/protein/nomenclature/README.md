A positional nomenclature map is made by `alignment_nomenclature.py` using a FASTA formatted sequence alignment. The nomenclature uses integer counts for each residue that is specified in the reference and additional integer count for positions that are not specified in the reference. For example:
| Index position | Named position | Amino Acid | Position Type |
|----------------|----------------|------------|---------------|
| 0 | 1.000 | A | major |
| 1 | 2.000 | K | major |
| 2 | 3.000 | G | major |
| 3 | 3.001 | - | minor/sub |
| 4 | 3.002 | - | minor/sub |
| 5 | 4.000 | L | major |

The nomenclature map is output using the name of the reference followed by `-nomenclature.csv`. For example, the nomenclature for accession QIS60846.1 as a reference will be named `QIS60846.1-nomenclature.csv`.

The three-digit sub-position format can acommodate up to 999 inserts in the reference sequence for an alignemnt.







fin.
