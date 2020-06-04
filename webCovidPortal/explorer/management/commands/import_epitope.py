import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from explorer.models import Protein, Alignment, Epitope;


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):
        # Concatenate rows from all taxa files and "insert if not exist" individually in a transaction.

        # field list
        fields = {
            'IEDB_ID':str,
            'protein':str,
            'alignment':str,
            'sequence':str,
            'offset':int,
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

        # get protein and alignment objects
        alns = {};
        pros = {};
        for a in Alignment.objects.filter(
            name__in=(records['alignment'].unique())
        ):
            alns[a.name] = a;
        for p in Protein.objects.filter(
            mesh_id__in=(records['protein'].unique())
        ):
            pros[p.mesh_id] = p;

        try:
            with transaction.atomic():
                for i,r in records.iterrows():
                    epi, created = Epitope.objects.get_or_create(
                        IEDB_ID     =r['IEDB_ID'],
                        protein     =pros[r['protein']],
                        alignment   =alns[str(r['alignment'])],
                        sequence    =r['sequence'],
                        offset      =r['offset'],
                    );
                    if created==False:
                        print(str(epi)+" exists");
        except: raise;
