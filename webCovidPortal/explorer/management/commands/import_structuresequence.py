import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from django.db.models import Value as V;
from django.db.models.functions import Concat;
from explorer.models import Alignment, Structure, StructureChain, StructureChainSequence;


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):

        # field list
        fields = {
            'pdb_id'        : str,
            'chain'         : str,
            'alignment'     : str,
            'offset'        : str,
            'sequence'      : str,
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
        records['_pdb_chain'] = records['pdb_id']+"."+records['chain'];

        # get alignments, chains.
        aligns = {};
        for a in Alignment.objects.filter(
            name__in=(records['alignment'].unique())
        ):
            aligns[a.name] = a;

        chains = {};
        for c in StructureChain.objects.annotate(
            pdb_chain=Concat('structure__pdb_id', V('.'), 'name')
        ).filter(
            pdb_chain__in=(records['_pdb_chain'])
        ):
            chains[c.pdb_chain] = c;

        try:
            with transaction.atomic():
                for i,r in records.iterrows():
                    if not r['_pdb_chain'] in chains:
                        raise Exception("No chain found for "+r['_pdb_chain']);
                    if not str(r['alignment']) in aligns:
                        raise Exception("No alignment found for "+r['_pdb_chain']);
                    scseq, created = StructureChainSequence.objects.get_or_create(
                        chain       = chains[ r['_pdb_chain'] ],
                        alignment   = aligns[ str(r['alignment']) ],
                        offset      = r['offset'],
                        sequence    = r['sequence'],
                    );

                    if created==False:
                        raise Exception(r['_pdb_chain']+" sequence already exists");
        except: raise;
        return;

        #
        #
        #
        # prots = {};
        # for p in Protein.objects.filter(
        #     mesh_id__in=(records['protein'].unique())
        # ):
        #     prots[p.mesh_id] = p;
        #
        # taxa = {};
        # for t in Taxon.objects.filter(
        #     gb_taxon_id__in=(records['taxon_id'].unique())
        # ):
        #     taxa[t.gb_taxon_id] = t;
        #
        # # create Structure and StructureChain
        # try:
        #     with transaction.atomic():
        #         for pdb in records['pdb_id'].unique():
        #             self.stdout.write(pdb);
        #             ss = records[records['pdb_id']==pdb];
        #             # verify one taxon
        #             if len(ss['taxon_id'].unique())!=1:
        #                 raise Exception("Multiple taxa defined for "+pdb);
        #             taxid = str(ss['taxon_id'].iloc[0]);
        #             if not taxid in taxa:
        #                 self.stdout.write(
        #                     "Taxon "+str(taxid)+" not found, skipping "+pdb);
        #                 continue;
        #             taxon = taxa[str(ss['taxon_id'].iloc[0])];
        #             struct, created = Structure.objects.get_or_create(
        #                 pdb_id      = pdb,
        #                 taxon       = taxon,
        #             );
        #             if created==False:
        #                 raise Exception(str(struct)+" exists");
        #             for c in ss['chain'].unique():
        #                 self.stdout.write(pdb+"."+c);
        #                 sss = ss[ss['chain']==c];
        #                 if len(sss['protein'].unique())!=1:
        #                     raise Exception(
        #                         "Multiple proteins defined for "+pdb+"."+chain
        #                     );
        #                 protein = None;
        #                 if sss['protein'].iloc[0] in prots:
        #                     protein = prots[sss['protein'].iloc[0]];
        #                 schain, created = StructureChain.objects.get_or_create(
        #                     structure = struct,
        #                     protein = protein,
        #                     name = c,
        #                 );
        #                 if created==False:
        #                     raise Exception(pdb+"."+chain+" exists");
        # except: raise;
