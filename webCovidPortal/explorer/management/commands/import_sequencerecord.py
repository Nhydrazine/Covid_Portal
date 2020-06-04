import os, sys, datetime, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from explorer.models import Protein, SequenceRecord, Taxon;
import pytz;

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):
        # Concatenate rows from all taxa files and "insert if not exist" individually in a transaction.

        # field list is manual due to foreign keys and autogenerators
        fields = {
            'protein'           : str,          # exepecting MeSH ID
            'taxon_id'          : str,
            'accession'         : str,
            'organism'          : str,
            'collection_date'   : str,
            'country'           : str,
            'host'              : str,
            'isolation_source'  : str,
            'isolate'           : str,
            'coded_by'          : str
        };

        records = []; # list of dataframes to concatenate
        for ffn in options['file']:
            # load file into dataframe
            if not os.path.isfile(ffn):
                self.stdout.write(ffn+" not found...");
                continue;
            df = pd.read_csv(ffn, dtype=fields);
            cols = df.columns.tolist();

            # check fields
            for field in fields.keys():
                if not field in cols:
                    raise Exception(ffn+" has no '"+field+"' column");

            records.append( df[fields.keys()] );
            self.stdout.write("Added "+str(len(df))+" records from "+ffn);
        records = pd.concat(records);

        # noneify nulls
        records = records.where(pd.notnull(records), None);


        # gather foreign key objects
        records['_f_protein_id'] = -1;
        f_proteins = {};
        records['_f_taxon_id'] = -1;
        f_taxa = {};

        for p in Protein.objects.filter(
            mesh_id__in=(records['protein'].unique())
        ):
            f_proteins[p.id] = p;
            ix = records[records['protein']==p.mesh_id].index;
            records.loc[ix,'_f_protein_id']=p.id;

        for t in Taxon.objects.filter(
            gb_taxon_id__in=(records['taxon_id'].unique())
        ):
            f_taxa[t.id] = t;
            ix = records[records['taxon_id']==t.gb_taxon_id].index;
            records.loc[ix,'_f_taxon_id']=t.id;

        unassigned = records[
            (records['_f_protein_id']<0) |
            (records['_f_taxon_id']<0)
        ];
        if len(unassigned)>0:
            raise Exception(
                "Foreign records could not be found for:\n"+str(unassigned));

        # trim to valid records only
        records = records[
            (records['_f_protein_id']>=0) &
            (records['_f_taxon_id']>=0)
        ];

        # parse collection date
        def format_date(d):
            if not d: return None;

            try:
                return pytz.utc.localize(
                    datetime.datetime.strptime(d,'%Y')
                );
            except:
                pass;

            try:
                return pytz.utc.localize(
                    datetime.datetime.strptime(d,'%d-%b-%Y')
                );
            except:
                pass;

            try:
                return pytz.utc.localize(
                    datetime.datetime.strptime(d,'%b-%Y')
                );
            except:
                pass;

            try:
                return pytz.utc.localize(
                    datetime.datetime.strptime(d,'%Y-%m-%d')
                );
            except:
                pass;

            try:
                return pytz.utc.localize(
                    datetime.datetime.strptime(d,'%Y-%m')
                );
            except:
                raise Exception("Can't interpret date: "+str(d));

        records['collection_date'] = records['collection_date'].apply(format_date);

        # noneify NaT's
        records['collection_date'] = \
            records['collection_date'].astype(object).where(
                records['collection_date'].notnull(), None
            );

        # "insert if not exists" in transaction
        try:
            with transaction.atomic():
                for i,r in records.iterrows():
                    o, created = SequenceRecord.objects.get_or_create(
                        protein = f_proteins[r['_f_protein_id']],
                        taxon = f_taxa[r['_f_taxon_id']],
                        accession = r['accession'],
                        organism = r['organism'],
                        collection_date = r['collection_date'],
                        country = r['country'],
                        host = r['host'],
                        isolation_source = r['isolation_source'],
                        isolate = r['isolate'],
                        coded_by = r['coded_by'],
                    );
                    if created==False:
                        print(str(o)+" exists");
        except: raise;
