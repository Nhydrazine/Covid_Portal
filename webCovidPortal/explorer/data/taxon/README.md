# Taxon Fetch

Taxon data comes from a page-source export of NCBI's taxon page for *betacoronavirus* (taxon id 694002) [https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=694002](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=694002). The source files should be named with the date they were generated as `taxonomy_results_[YYYYMMDD].html`.

These HTML sources are parsed using `taxonomy_parser.py` (set the `infile` variable), which generates a csv export called `taxonomy_parsed.csv` with the follwing columns:

| column | required* | type | description |
|--------|----------|------|-------------|
| leaf | yes | boolean | `True` if taxon is a leaf, `false` if node (has children). |
| path | yes |str | `.`-joined list of parental taxon IDs starting at the most ancestral (left) to the most recent (right). |
| gb_taxon_id | yes | str | NCBI Taxon ID |
| name | yes | str | Name of the taxon |
| level | yes | str | Taxon level (e.g. `subgenus` or `species` etc...) |
| type | no | str | `circle` or `square`depending on HTML list type. This confirms leaf or node. |
| href | no | str | URL link provided for the proteins page of the Taxon |
| plink | no | str | URL link to NCBI protein database listing proteins for the Taxon |
| pcount | no | int | Number of protein database entries for the Taxon |

**required for importing a taxon into the database.*
