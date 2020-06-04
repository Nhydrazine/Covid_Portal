import os, sys, re, datetime, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from explorer.models import Alignment, SequenceRecord, Sequence;
import pytz;

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):
        # Concatenate rows from all taxa files and "insert if not exist" individually in a transaction.

        # field list is manual due to foreign keys and autogenerators
        fields = {
            'alignment':str,    # name of an alignment in Alignment table
            'accession':str,    # genbank accession (to match SequencRecord)
            'sequence':str,     # aligned sequence
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
        records['_f_alignment_id'] = -1;
        f_alignments = {};
        records['_f_sequencerecord_id'] = -1;
        f_sequencerecords = {};

        for a in Alignment.objects.filter(
            name__in=(records['alignment'].unique())
        ):
            f_alignments[a.id] = a;
            ix = records[records['alignment']==a.name].index;
            records.loc[ix,'_f_alignment_id']=a.id;

        for sr in SequenceRecord.objects.filter(
            accession__in=(records['accession'].unique())
        ):
            f_sequencerecords[sr.id] = sr;
            ix = records[records['accession']==sr.accession].index;
            records.loc[ix,'_f_sequencerecord_id']=sr.id;

        unassigned = records[
            (records['_f_alignment_id']<0) |
            (records['_f_sequencerecord_id']<0)
        ];
        if len(unassigned)>0:
            raise Exception(
                "Foreign records could not be found for:\n"+str(unassigned));

        # trim to valid records only
        records = records[
            (records['_f_alignment_id']>=0) &
            (records['_f_sequencerecord_id']>=0)
        ];

        # handle offset
        records['offset'] = 0;
        trim_rx = re.compile('^(\-+)(.*)(\-+)$');

        for ix in records.index:
            m = re.match(trim_rx, records.loc[ix,'sequence']);
            if m:
                records.loc[ix,'offset'] = len(m.group(1));
                records.loc[ix,'sequence'] = m.group(2);

        # "insert if not exists" in transaction
        try:
            with transaction.atomic():
                for i,r in records.iterrows():
                    o, created = Sequence.objects.get_or_create(
                        sequence_record = f_sequencerecords[
                            r['_f_sequencerecord_id']],
                        alignment = f_alignments[
                            r['_f_alignment_id']],
                        sequence = r['sequence'],
                        offset = r['offset'],
                    );
                    if created==False:
                        print(str(o)+" exists");
        except: raise;
