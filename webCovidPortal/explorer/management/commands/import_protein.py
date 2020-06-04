import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from explorer.models import Protein;


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):
        # Concatenate rows from all taxa files and "insert if not exist" individually in a transaction.

        # get field list
        fields = \
        [f.name for f in Protein._meta.fields
        if type(f)!=type(models.AutoField())];

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

        # "insert if not exists" in transaction
        try:
            with transaction.atomic():
                for i,r in records.iterrows():
                    t, created = Protein.objects.get_or_create(
                        **dict(zip(fields, r[fields]))
                    );
                    if created==False:
                        print(str(t)+" exists");
        except: raise;
