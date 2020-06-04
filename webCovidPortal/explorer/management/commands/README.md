# Custom Manager Commands

The custom Django manager commands described here are used for formatting and importing data into the CoronaWhy Protein Explorer database. These data are gathered by other scripts, which are not described here.

## Initial Population

The database is initially populated in the following order:
1. Import taxa using `import_taxa`.
2. Import proteins using `import_protein` (generic for organism group e.g. Coronavirus Spike, or HIV Env).
3. Import sequence records using `import_sequencerecord` (GenBank metadata, not the sequences themselves, references protein by MeSH ID).
4. Import alignments using `import_alignment` (names that group sequences by alignment, references protein by MeSH ID).
5. Import aligned sequences using `import_sequence`. referencing protein by MeSH, sequence record by NCBI Accession and alignment by name.

Then you can:

### Import Epitope Sequences/Experimental Data

1. Align epitopes to a sequence alignment by referencing alignment by name, protein by MeSH ID. *Only contiguous epitopes can be aligned for now*.
2. Import aligned epitope sequences using `import_eptope`.
3. Import epitope experiments using `import_epitopeexperiment` referencing epitope by IEDB_ID.

### Import Alignment Nomenclatures

1. Generate your nomencalture and import using `import_nomenclature`, referencing an alignment, protein, and reference sequence.


## Importing Taxa
The `import_taxa` command imports a CSV Taxon file containing taxon information into the Protein Explorer database. The realted Django model is `explorer.models.Taxon`

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| gb_taxon_id     | str       | NCBI Taxon ID. |
| leaf            | boolean   | True is leaf, False is node. |
| path            | str       | Period separated list of ancestral taxon IDs starting with the most ancestral (left to right). |
| level           | str       | Phylogenetic level (e.g. Genus, Family etc...). |
| name            | str       | Name of the taxon. |

### Usage
`python manager.py import_taxa [CSV TAXON FILE]`



## Importing Proteins
The `import_protein` command imports a CSV Protein file containing information about a protein. The realted Django model is `explorer.models.Protein`

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| name            | str       | Protein name. |
| mesh_id         | str       | NCBI MeSH ID. |

### Usage
`python manager.py import_protein [CSV PROTEIN FILE]`



## Importing Sequence Records
The `import_sequencerecord` command imports a CSV file containing information about protein sequences that you will import separately. The realted Django model is `explorer.models.SequenceRecord`

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| protein         | str       | Protein NCBI MeSH ID that sequence record will be linked to. The corresponding MeSH ID must exist in Protein table. |
| taxon_id        | str       | NCBI Taxon ID for the taxon that this sequence belongs to, the Taxon must exist in the Taxon table. |
| accession       | str       | NCBI accession number of sequence including version (e.g. XXXXX.#). |
| organism        | str       | Name of the organism. |
| collection_date | str       | Date the sequence was obtained (null). |
| country         | str       | Country or country:region the sequence was obtained from (null). |
| host            | str       | For pathogens, name of the host that this organism was obtained from (null). |
| isolation_source| str       | Name of the tissue the sequence was obtained from (null). |
| isolate         | str       | Name of the viral isolate this sequence refers to. |
| coded_by        | str       | NCBI Nucleotide sequence region and accession number that codes for this protein sequence. |

### Usage
`python manager.py import_sequencerecord [CSV FILE]`



## Importing Alignments
An alignment groups together multiple sequence that have been adjusted so that the positons of letters across the sequences are *normalized* based on a consensus pattern among them - this allows, for example, everyone to agree on what positions are part of various structural landmarks in a protein. The realted Django model is `explorer.models.Alignment`

To import an actual sequence, the sequence must first be aligned and and a name for the alignment must be assigned so that the sequence is only compared with other sequences belonging to the same alignment.

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| name            | str       | Name for the alignment. |
| protein         | str       | NCBI MeSH ID of the protein the alignment belongs to, the MeSH ID should exist in the Protein table. |

### Usage
`python manager.py import_alignment [CSV FILE]`



## Importing Sequences
The `import_sequence` command imports a CSV file containing **aligned** protein sequence information. The realted Django model is `explorer.models.Sequence`.

**DO NOT IMPORT SEQUENCES THAT HAVE NOT BEEN ALIGNED**.

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| alignment       | str       | Name of alignment for this sequence (must be in Alignment table). |
| accession       | str       | NCBI accession number including version (e.g. XXXXX.#) of the sequence record this sequence belongs to. The sequence record must exist. |
| sequence        | str       | Aligned sequence string. |

### Usage
`python manager.py import_sequence [CSV FILE]`



## Aligning Epitopes
Epitope alignments are currently performed by exact matching against sequence alignments that exist in the database. This works well for contiguous epitope sequences but does not work for discontiguous ones.

The `align_epitopes` command uses and exact-matching strategy to align epitopes to sequences belonging to an existing alignment. The process is as follows:

1. Perform a database search for the epitope pattern among aligned sequences belonging to the desired alignment. The search dealigns the sequences before checking for the match. The first exact match is obtained. If no match is found the epitope is skipped and no alignment will be made.
2. Alignment-appropriate gaps are inserted into the epitope sequence using a Pandas indexing method.
3. The aligned epitope sequence is stored along with required information needed for the `import_epitope` command.

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| protein         | str       | NCBI MeSH ID for the protein this epitope belongs to. |
| IEDB_ID         | str       | IEDB ID for the epitope. |
| sequence        | str       | unaligned contiguous epitope sequence. |
| alignment       | str       | name of the alignment you want the aligned epitope to conform to. You must have sequences belonging to the appropriate protein and alignment. |

### Usage
`python manager.py align_epitopes [EPITOPE CSV FILE] [OUTPUT CSV FILE]`



## Importing Epitopes
Once epitope sequences are aligned, they can be imported using the `import_epitope` command. The relevant Django model is `explorer.models.Epitope`.

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| protein         | str       | NCBI MeSH ID for the protein this epitope belongs to. |
| IEDB_ID         | str       | IEDB ID for the epitope. |
| alignment       | str       | name of the alignment you want the aligned epitope to conform to. You must have sequences belonging to the appropriate protein and alignment. |
| sequence        | str       | aligned contiguous epitope sequence with gaps as needed. |
| offset          | str       | Start position of epitope sequence in the alignment. |

### Usage
`python manager.py import_epitope [CSV FILE]`



## Importing Epitope Experiments
Once epitope sequences are aligned, they can be imported using the `import_epitope` command. The relevant Django model is `explorer.models.EpitopeEpxeriment`.

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| IEDB_ID         | str       | IEDB ID for the epitope |
| host            | str       | The name of the host organism used for the experiment. |
| assay_type      | str       | Name of the assay type (e.g. "ELISA"). |
| assay_result    | str       | Result of the assay (single-word categorical description). |
| mhc_allele      | str       | Four-digit resolved HLA recognizing the epitope. |
| mhc_class       | str       | MHC class tested (I is T cell, II is B cell). |
| exp_method      | str       | Experimental method used (subclass of assay type). |
| measurement_type| str       | Type of measurement (binding, lysis activity etc...). |

### Usage
`python manager.py import_epitopeexperiment [CSV PROTEIN FILE]`



## Importing Nomenclatures
While an alignment normalizes the postions of letters in a sequence using a consensus approach, a position nomenclature gives a name to each position relative to a common reference sequence in the alignment. A nomenclature contains major positions where a letter is present in the reference sequence, and minor positions where the reference has a gap, indicating that there is no letter there.

Nomenclatures are generated using a nomenclature generator script, or they can be made manually. The Protein Explorer tracks only integer major/minor positions. The formatting of those position names are left to the user (e.g. use a, b, c, d or 001, 002, 003 for minor position names?).

The relevant Django models are `explorer.models.Nomenclature` (for description of the nomenclature and its alignment) and `explorer.models.NomenclaturePosition` (for the actual major/minor position indices).

### Required Columns
| Column          | type      | Description |
|-----------------|-----------|-------------|
| protein         | str       | MeSH ID for the protein the nomenclature describes. |
| alignment_name  | str       | Name of the alignment this nomenclature belongs to. |
| name            | str       | A name for the nomenclature. |
| reference       | str       | NCBI Accession number (including version, e.g. XXXXX.#) of the reference sequence. Reference sequence must exist in database. |
| major           | int       | Major position. |
| minor           | int       | Minor position. |

### Usage
`python manager.py import_nomenclature [CSV FILE]`




fin.
