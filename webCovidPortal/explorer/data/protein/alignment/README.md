| file | description |
|------|-------------|
|`clustalo-E20200519-140102-0914-92371964-p1m.output`| ClustalO output (text) |
|`clustalo-E20200519-140102-0914-92371964-p1m.clustal_num` | Alignment (text) |
|`clustalo-E20200519-140102-0914-92371964-p1m.dnd`| Guide tree dendrogram (Newick) |
|`clustalo-E20200519-140102-0914-92371964-p1m.ph` | Phylogenetic tree (Newick)|
| `clustalo-E20200519-140102-0914-92371964-p1m.pim`| Percent identity matrix (text) |

Filtered sequence file `../gbs_foralignment_byaccession.fasta` was aligned using ClustalO via. [EMBL-EBI search and sequence analysis tools APIs in 2019](https://www.ebi.ac.uk/Tools/msa/clustalo/). The resulting alignment file was converted back to FASTA and CSV formats with sequences named by `[ACCESSION].[VERSION]` using `clustal_to_fasta.py` and `clustal_to_csv.py`, respectively.

Also, the ClustalO phylogenetic tree was converted to named organisms using `phylo_accession_to_name.py` to create `named_phylogeny.tre` (Newick).

fin.
