Epitope information was sourced from [ViPR](https://www.viprbrc.org/brc/home.spg?decorator=vipr) via. the query matching family *Coronaviridae* and subfamily *Orthocoronavirinae* and genus *BetacoronavirusSelect*, for experimentally verified results, with the remaining search parameters being empty or at default setting.



As of May 16, 2020 this returned 1,779 results that were saved in excel format and then csv format as `VIPR-EXPORT-20200516.csv`. Note that the columns in each row break down further, by commas, into individual experiments. The columns in this file are:

| Column Name | Description |
|-------------|-------------|
IEDB ID	| Unique identifier for IEDB |
Epitope Sequence | Amino acid sequence |
Protein Names | Name of target proteins (S, N etc...) |
Host | Host species |
Assay Type Category | Type of assay |
Assay Result | Assay result (Positive, Positive-Low, Positive-Intermediate, Positive-High, Negative) |
MHC Allele Name | Name of MHC allele (4-digit resolution) |
MHC Allele Class | MHC I or II |
Method | Experimental assay type |
Measurement | Measurement type |

Comma-joined entries from `VIPR-EXPORT-20200516.csv` were expanded using `epitope_parser.py` to yield `VIPR-EXPORT-20200516-EXPANDED.csv`.

Distinct *Protein Name* entries were extracted from `VIPR-EXPORT-20200516.csv` using `distinct_protein_names.py` to yield `VIPR-EXPORT-20200516-PNAMES.csv`. Names associated with the spike glycoprotein were manually indicated in a boolean column called *Spike Synonym* that was added, and saved as `VIPR-EXPORT-20200516-PNAMES-MARKED.csv`.

Records from `VIPR-EXPORT-20200516-EXPANDED.csv` were restricted to valid spike synonyms using `VIPR-EXPORT-20200516-PNAMES-MARKED.csv` and all restricted *Protein Name* entries were normalized to the MeSH heading `Spike Glycoprotein, Coronavirus`.

For entry into database, a table with the column headers described above will be needed, along with an additional column that specifies the start location of each epitope relative to whatever alignment reference will be used.

fin.
