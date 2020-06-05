# Explorer Data Folder

This folder contains scripts that gather and/or process various types of data that are needed for the explorer. See documentation in each folder for specifics. Each data type object is in a seprate folder:

| Folder | Model(s) | Description |
|--------|----------|-------------|
| `cleaning` | N/A | Auxiliary folder for temporary storage of data that's being cleaned up, inspected or modified. |
| `epitope` | `explorer.models.Epitope`, `explorer.models.EpitopeExperiment` | B/T-cell epitopes and epitope experiment data from ViPR and IEDB. |
| `imports` | N/A | For storing CSV files that are cleaned and ready to import. |
| `protein` | `explorer.models.SequenceRecord`, `explorer.models.Sequence`, `explorer.models.Nomenclature`, `explorer.models.NomenClaturePosition` | Downloading and processing NCBI protein sequences, running alignments of those sequences and calculating position nomenclatures. |
| `structure` | `explorer.models.Structure`. `explorer.models.StructureChain`, `explorer.models.StructureChainSequence`, `explorer.models.StructureChainResidue`, `explorer.models.StructureAtom` | Extracting and aligning structure sequence data and atomic coordinates. |
| `taxon` | `explorer.models.Taxon` | NCBI taxonomy data processing. |
