import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from explorer.models import Epitope, EpitopeExperiment;


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):
        # Concatenate rows from all taxa files and "insert if not exist" individually in a transaction.

        # field list
        fields = {
            'IEDB_ID':str,
            'host':str,
            'assay_type':str,
            'assay_result':str,
            'mhc_allele':str,
            'mhc_class':str,
            'exp_method':str,
            'measurement_type':str
        };

        records = []; # list of taxon dataframes to concatenate
        for ffn in options['file']:
            # load file into dataframe
            if not os.path.isfile(ffn):
                self.stdout.write(ffn+" not found...");
                continue;
            df = pd.read_csv(ffn);
            cols = df.columns.tolist();

            # check fields
            for field in fields:
                if not field in cols:
                    raise Exception(ffn+" has no '"+field+"' column");

            records.append( df[fields] );
            self.stdout.write("Added "+str(len(df))+" records from "+ffn);
        records = pd.concat(records);
        records = records.replace('-N/A-',"");
        records = records.drop_duplicates();

        # get epitope objects
        epis = {};
        for e in Epitope.objects.filter(
            IEDB_ID__in=(records['IEDB_ID'])
        ):
            epis[e.IEDB_ID] = e;

        # remove epitopes that weren't found
        z = pd.Series(records['IEDB_ID'].unique());
        z.index = z;
        z = z.isin(epis.keys());
        records = records[~records['IEDB_ID'].isin( z[z==False].index )];
        self.stdout.write("The following IEDB_IDs were not found:");
        self.stdout.write(','.join(z[z==False].index.astype(str)));

        try:
            with transaction.atomic():
                for i,r in records.iterrows():
                    epix, created = EpitopeExperiment.objects.get_or_create(
                        epitope             = epis[str(r['IEDB_ID'])],
                        host                = r['host'],
                        assay_type          = r['assay_type'],
                        assay_result        = r['assay_result'],
                        mhc_allele          = r['mhc_allele'],
                        mhc_class           = r['mhc_class'],
                        exp_method          = r['exp_method'],
                        measurement_type    = r['measurement_type']
                    );
                    if created==False:
                        print(str(epix)+" exists");
                    else:
                        print(str(epix)+" created");
        except: raise;
