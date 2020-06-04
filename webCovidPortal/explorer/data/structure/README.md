# Crystal Structure Extraction

The overall population of crystal structure data is as follows:

1. Download PDB files (this is manual for now).
2. Identify chain IDs for your protein of interest.
    * `downloads/[pdb files] -< extract_chains.py -> chains.csv`
3. Extract priamary structure data.
    * `chains.csv -< extract_primary.py -> atoms.csv`
4. Extract secondary structure data.
    * `chains.csv -< extract_secondary.py -> helices.csv, sheets.csv`
5. Derive sequence from primary structure including the provided positional nomenclature.
    * `atoms.csv -< build_sequence.py -> sequences.csv`
6. Align sequence with target alignment we're using
    * See documentation in the `./alignments` folder, alignment requires the `chains.csv` file and `sequences.csv` file from this folder.
    * Alignment will produce a single file called `conformed_alignments.csv`, which is used to produce final import files.
7. Generate a position-conversion map between provided nomenclature and our alignment for remapping.
    * This is given by the relationship between `resid` (structure index for residue) and `resix` (residue index in unaligned, ungapped structure sequence) columns in the final import residue file.
8. Build CSV files to be imported into django models using `build_imports.py`, which requires `./chains.csv`, `./atoms.csv`, and `./alignment/conformed_alignments.csv`. The outputs are:
    * `./imports/structureChains.csv` for `explorer.models.Structure` and `explorer.models.StructureChain`
    * `./imports/structureSequences.csv` for `explorer.models.StructureSequence`
    * `./imports/structureAtoms.csv` for `explorer.models.StructureAtom`
9. Store remapped secondary structure features (probably as a string of `H,S,U`) (`TBD`).

## Download Structure PDB Files
Currently, crystal structure PDB files are downloaded manually from [RCSB](https://www.rcsb.org) because we have not yet identified good search criteria to isolate only coronavirus spike structures. PDB files are stored in the `downloads` folder for processing.

## Extract List of Chain IDs
Crystal structures often contain additional proteins used to stabilize the protein of interest, or to investigate interactions. Usually, each protein is stored as one or more chains in the structure (PDB) file. Chain IDs for all crystal structure files in the `downloads` folder are extracted with `extract_chains.py`, which generates a CSV file called `chains.csv` with the following:

| column | type | description |
|--------|------|-------------|
| pdb_id    | str   | PDB ID of the structure. |
| mol_id    | int   | Molecule ID for the chain. |
| mol_name  | str   | Molecule name for the chain. |
| chain     | char  | Chain ID. |

## Extract Primary Structure
Primary structure information includes the amino acid sequence and spatial coordinates of atoms from each amino acid. Primary structure data is extracted with `extract_primary.py`, using `chains.csv` to limit extraction to only the chains that belong to the relevant molecule. The variable `use_chains` is a list of valid molecule names whose primary structures will be extracted.

**Note** that multiple chains per molecule is not currently supported.

Because each residue consists of several atoms, the desired atoms to extract are specified in the `use_atoms` variable. These names follow the standard nomenclature, which can be found [here on page 27](https://cdn.rcsb.org/wwpdb/docs/documentation/file-format/PDB_format_1992.pdf). Only the atoms with names listed in `use_atoms` will be extracted.

The output is a CSV file called `atoms.csv` with the following:

| column | type | description |
|--------|------|-------------|
| pdb       | str   | PDB ID of the structure. |
| atom      | str   | Name of the atom. |
| resname   | str   | Three letter amino acid name. |
| chain     | char  | Chain ID. |
| resid     | int   | Residue number (according to positional nomenclature decided by author). |
| icode     | char  | Insert code (usually blank). |
| element   | char  | Name of the element. |
| charge    | int   | Charge of the atom. |
| occupancy | float | Occupancy of atom. |
| x         | float | *x* coordinate. |
| y         | float | *y* coordinate. |
| z         | float | *z* coordinate. |

## Extract Secondary Structure
Secondary structure describes local spatial arrangements that occur along the linear peptide sequence, primarily *alpha helices* and *beta sheets*. These structural features are extracted using the `SHEET` and `HELIX` lines of a PDB file by `extract_secondary.py`, which is also guided by `chains.csv` to limit extraction to relevant chains only. **Note** that this script has the same `use_chains` list as described for `extract_primary.py`. The script outputs a CSV file called `sheets.csv` with the following:

| column | type | description |
|--------|------|-------------|
| pdb               | str   | PDB ID of the structure. |
| sheet             | str   | An ID/name for the sheet. |
| strand            | int   | Strand within the sheet. |
| start_chain       | char  | Chain that the sheet starts on. |
| end_chain         | char  | Chain that the sheet ends on. |
| start_resname     | str   | Three letter amino acid the strand starts with. |
| end_resname       | str   | Three letter amino acid the strand ends with. |
| start_resid       | int   | Residue number strand starts with(!). |
| end_resid         | int   | Residue number strand ends with(!). |

*(!) see resid under Extract Primary Structure*

As well as a CSV file called `helices.csv` with the following:

| column | type | description |
|--------|------|-------------|
| pdb               | str   | PDB ID of the structure. |
| helix             | str   | An ID/name for the helix. |
| serial            | int   | Serial number for helix. |
| start_chain       | char  | Chain that the helix starts on. |
| end_chain         | char  | Chain that the helix ends on. |
| start_resname     | str   | Three letter amino acid the strand helix with. |
| end_resname       | str   | Three letter amino acid the strand helix with. |
| start_resid       | int   | Residue number helix starts with(!). |
| end_resid         | int   | Residue number helix ends with(!). |

*(!) see resid under Extract Primary Structure*

## Build Amino Acid Sequence with Postional Nomenclature
Single-letter amino acid sequences are made with `build_sequence.py` using `atoms.csv`. In addition, the `resid` for each amino acid is stored so that any given positional nomenclature can be preserved for comparison later on. The output is `sequences.csv` with the following columns:

| column | type | description |
|--------|------|-------------|
| pdb               | str   | PDB ID of the structure. |
| chain             | char  | Chain ID. |
| sequence          | str   | Amino acid single-letter sequence. |
| position          | str   | Comma-separated list of residue IDs corresponding to characters in sequence. |

## Alignment

See README.md in the `alignment` folder.

## Build Imports

Importable CSV files are generated by `build_imports.py` with the following columns:

### structureChains.csv
Is used to populate `explorer.models.Structure` and `explorer.models.StructureChain`.

| column | type | description |
|--------|------|-------------|
| pdb_id                | str   | PDB ID of the structure. |
| taxon_id              | str   | NCBI Taxon ID of the structure. |
| protein               | str   | MeSH ID of protein (hard coded in `build_imports.py` for now). |
| chain                 | char  | Chain ID. |

### structureSequences.csv
Is used to populate `explorer.models.StructureSequence`.

| column | type | description |
|--------|------|-------------|
| pdb_id                | str   | PDB ID of the structure. |
| chain                 | char  | Chain ID. |
| alignment             | str   | Name of reference alignment used. |
| offset                | int   | Offset of sequence to alignment. |
| sequence              | str   | The amino acid sequence. |

### structureAtoms.csv
Is used to populate `explorer.models.StructureAtom`.

| column | type | description |
|--------|------|-------------|
| pdb_id        | str   | PDB ID of the structure. |
| chain         | char  | Chain ID. |
| resix         | int   | Index of atom's residue relative to unaligned, ungapped amino acid sequence. |
| resid         | int   | ID of residue in crystal structure chain. |
| resn          | char  | Single-letter amino acid code of atom's residue. |
| atom          | str   | Name of atom in residue. |
| element       | str   | Symbol of the atomic element. |
| charge        | int   | Ionic charge of atom. |
| occupancy     | float | Atomic occupancy. |
| x             | float | Atom's *x* position. |
| y             | float | Atom's *y* position. |
| z             | float | Atom's *z* position. |

**NOTE** that `resix` and `resid` map from ungapped sequence characters to crystal structure residue numbers (using whatever positional nomenclature the authors of the PDB file chose to use). This relationship is important to maintain so that users can locate these residues in the actual PDB files.








fin.
