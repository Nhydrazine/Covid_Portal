import os, sys, re, datetime, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from django.db.models import Value;
from django.db.models.functions import Replace;
from explorer.models import Alignment, Protein, SequenceRecord, Sequence, Epitope;
import pytz;

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str );
        parser.add_argument('outfile', type=str );

    def handle(self, *args, **options):
        # Concatenate rows from all taxa files and "insert if not exist" individually in a transaction.

        # field list is manual due to foreign keys and autogenerators
        fields = {
            'protein':str, # expect MeSH ID
            'IEDB_ID':str,
            'sequence':str,
            'alignment':str,
            # 'host':str,
            # 'assay_type':str,
            # 'assay_result':str,
            # 'mhc_allele':str,
            # 'mhc_class':str,
            # 'exp_method':str,
            # 'measurement_type':str
        };

        # load file into dataframe
        records = pd.read_csv(options['file'], dtype=fields)[fields.keys()];
        cols = records.columns.tolist();

        # check fields
        for field in fields.keys():
            if not field in cols:
                raise Exception(ffn+" has no '"+field+"' column");

        # trim to distinct epitopes only
        records = records.drop_duplicates(subset=['IEDB_ID']);
        self.stdout.write("Added "+str(len(records))+" records from "+options['file']);

        # for now, remove discontiguous and single-residue epitopes
        # which will require more sophistocated methods
        dc_ix = records[
            (~records['sequence'].str.contains(',')) &
            (~records['sequence'].str.contains(r'\d'))
        ].index;
        records = records.loc[dc_ix];
        records = records.replace('-N/A-',"");
        self.stdout.write("Dropping discontiguous epitopes...");

        # retrieve alignments and proteins
        alns = {};
        pros = {};
        for aln in Alignment.objects.filter(
            name__in=records['alignment'].unique()
        ):
            alns[aln.name] = aln;
        for pro in Protein.objects.filter(
            mesh_id__in=records['protein'].unique()
        ):
            pros[pro.mesh_id] = pro;

        aligned_epitopes = []; # list of dicts to be dataframed

        for i,r in records.iterrows():
            try:
                seq = Sequence.objects.filter(
                    sequence_record__protein__mesh_id__contains=r['protein']
                ).annotate(
                    dealigned=Replace(
                        'sequence',
                        Value('-'),
                        Value(''))
                ).filter(
                    dealigned__icontains=r['sequence']
                )[0];
            except:
                # need partial pattern matching to align
                self.stdout.write("No exact match for "+r['sequence']);
                continue;

            # found exact matching sequence
            # now align epitope to sequence alignment by mapping to
            # alignment indices of the dealigned sequence.

            # map alignment indices to dealigned sequence
            aln_series = pd.Series(list(seq.sequence));
            dln_series = aln_series[aln_series!='-'];

            # get offset of epitope pattern in dealigned sequence
            dln_epitope_offset = len(seq.dealigned.split(r['sequence'])[0]);

            # subset alignment indices for epitope starting at offset and
            # going for the length of pattern (only works for continuous
            # epitope patterns).
            epi_index = dln_series.index[
                dln_epitope_offset:dln_epitope_offset+len(r['sequence'])
            ];

            # fill epitope with appropriate gaps from alignment
            epi_aligned = [];
            for i in range(epi_index.min(), epi_index.max()+1):
                if i in epi_index:
                    epi_aligned.append(aln_series[i]);
                else:
                    epi_aligned.append('-');

            # store
            aligned_epitopes.append({
                'IEDB_ID'           : r['IEDB_ID'],
                'protein'           : pros[r['protein']].mesh_id,
                'alignment'         : alns[r['alignment']].name,
                'matched'           : seq.sequence_record.accession,
                'sequence'          : ''.join(epi_aligned),
                'offset'            : dln_epitope_offset,
                # 'host'              : r['host'],
                # 'assay_type'        : r['assay_type'],
                # 'assay_result'      : r['assay_result'],
                # 'mhc_allele'        : r['mhc_allele'],
                # 'mhc_class'         : r['mhc_class'],
                # 'exp_method'        : r['exp_method'],
                # 'measurement_type'  : r['measurement_type'],
            });
            self.stdout.write("Exact match for "+r['sequence']);

        # write
        aligned_epitopes = pd.DataFrame(aligned_epitopes);
        aligned_epitopes.to_csv(options['outfile']);
        self.stdout.write("Written to "+options['outfile']);
