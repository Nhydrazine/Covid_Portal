import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from explorer.models import Alignment, Protein;


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):
        # Concatenate rows from all taxa files and "insert if not exist" individually in a transaction.

        # field list is manual due to foreign keys and autogenerators
        fields = ['name','protein'];
        # expect protein to me a MeSH ID.

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

        # assign protein IDs or throw
        records['protein_id'] = -1;
        proteins = {};  # distinct protein objects for insert later
        for p in Protein.objects.filter(
            mesh_id__in=(records['protein'].unique())
        ):
            proteins[p.id] = p;
            ix = records[records['protein']==p.mesh_id].index;
            records.loc[ix,'protein_id'] = p.id;
        unassigned = records[records['protein_id']<0];
        if len(unassigned)>0:
            raise Exception(
                "Protein records could not be found for:\n"+str(unassigned));

        # "insert if not exists" in transaction
        records = records[records['protein_id']>=0];    # filter
        records = records[['name','protein_id']];       # trim

        try:
            with transaction.atomic():
                for i,r in records.iterrows():
                    t, created = Alignment.objects.get_or_create(
                        name = r['name'],
                        protein = proteins[r['protein_id']]
                    );
                    if created==False:
                        print(str(t)+" exists");
        except: raise;
