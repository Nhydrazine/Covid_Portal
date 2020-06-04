echo importing taxa
python manage.py import_taxa explorer/data/taxon/taxonomy_parsed.csv

echo importing proteins
python manage.py import_protein explorer/data/initial_protein.csv

echo importing alignments
python manage.py import_alignment explorer/data/initial_alignment.csv

echo importing sequence records
python manage.py import_sequencerecord explorer/data/spike_sequence_records.csv

echo importing sequence alignments
python manage.py import_sequence explorer/data/spike_sequence_alignment_20200505.csv

echo importing epitope alignments
python manage.py import_epitope explorer/data/aligned_epitopes.csv

echo importing epitope experiments
python manage.py import_epitopeexperiment explorer/data/epitopes_experiments.csv

echo importing nomenclature
python manage.py import_nomenclature explorer/data/HKU-N2_nomenclature.csv
