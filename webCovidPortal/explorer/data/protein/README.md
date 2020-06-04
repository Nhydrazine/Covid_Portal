
# Protein Fetch and Process

## Fetch Protein Sequences

`fetch_protein_gbs_from_taxon_ids.py` searches for proteins using individual taxon id's from a csv file with (at minimum) the following columns:

| column | type | description |
|--------|------|-------------|
| gb_taxon_id | str | NCBI taxon id |
| leaf | boolean | `True`if taxon is a leaf, `False` if a node (has children) |
| pcount | int | Number of expected NCBI protein records for the taxon |

Note that **only leaf taxons are used** because nodes contain multiple leafs.

GenBank protein records for the `gb_taxon_id`s are searched and fetched using NCBI's **esearch** and **efetch** APIs, respectively. GenBank records are output to `fetched_proteins.fna` and taxon IDs that failed the search/fetch are output to `failed_fetch_taxa.csv`. A one-second delay is built in between each fetch as required by NCBI.

## Extract Protein Sequence Information

Protein sequences and their metadata are extracted from `fetched_proteins.fna` using `extract_protein_sequences.py`, generating `gb_extract.csv` with the following columns:

| column | type | description |
|--------|------|-------------|
| taxon_id                | str | NCBI Taxon ID for the sequence |
| description             | str | descriptive name of the sequence |
| accession               | str | GenBank accession, not including version |
| organism                | str | Name of the organism sequence belongs to |
| version                 | str | GenBank accession with version |
| seq                     | str | Raw protein sequence |
| references              | str | Array of PubMed IDs for sequence |
| collection_date         | str | Date sequence was collected |
| country                 | str | Country/Region sequence was collected from |
| host                    | str | Host organism |
| isolation_source        | str | Tissue the sequence was isolated from |
| coded_by                | str | GenBank Accession:Region for nucleotide coding region |
| isolate                 | str | Name of viral isolate where specified. (*Note the isolate may also be contained in the organism or description field*). |

**IMPORTANT** `extract_protein_sequences.py` has a hard-coded list called `invalids`, which are accession/version numbers that have been manually determined to not be the protein of interest despite the search criteria. Sequences with these accession numbers are not extracted.

**IMPORTANT** All spike sequences listed as *hypothetical* or *putative* are excluded.

## Build FASTA for Alignment

A FASTA file for aligning the sequences is produced by `build_fasta_for_alignment.py`, which generates `gb_foralignment_byaccession.fasta`.

## Sequence Alignment

FASTA sequences are aligned using Clustal Omega at the [EMBL-EBI search and sequence analysis tools APIs in 2019](https://www.ebi.ac.uk/Tools/msa/clustalo/) and alignment outputs were stored in the `alignment` folder.

## Alignment Nomenclature

Nomenclatures are constructed using `nomenclature/alignment_nomenclature.py` with the reference sequence identified by accession number (including version). Nomenclatures are output as CSV files.

# Notes

* First identified SARS-CoV-2 from Wuhan is YP_009724390.1. This is used as a reference for CoV-2. I think we should choose a SARS-CoV for reference to emphasize changes and inserts (particularly the furin cleavage site inserts).

* Using HKU1 Strain N2 (Q14EB0.1) for nomenclature reference.
