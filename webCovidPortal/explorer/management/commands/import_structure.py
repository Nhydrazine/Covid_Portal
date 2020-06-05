import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from explorer.models import Protein, Taxon, Structure, StructureChain;


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):

        # field list
        fields = {
            'pdb_id'        : str,
            'taxon_id'      : str,
            'protein'       : str,
            'chain'         : str,
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
        # get proteins and taxa
        prots = {};
        for p in Protein.objects.filter(
            mesh_id__in=(records['protein'].unique())
        ):
            prots[p.mesh_id] = p;

        taxa = {};
        for t in Taxon.objects.filter(
            gb_taxon_id__in=(records['taxon_id'].unique())
        ):
            taxa[t.gb_taxon_id] = t;

        # create Structure and StructureChain
        try:
            with transaction.atomic():
                for pdb in records['pdb_id'].unique():
                    self.stdout.write(pdb);
                    ss = records[records['pdb_id']==pdb];
                    # verify one taxon
                    if len(ss['taxon_id'].unique())!=1:
                        raise Exception("Multiple taxa defined for "+pdb);
                    taxid = str(ss['taxon_id'].iloc[0]);
                    if not taxid in taxa:
                        self.stdout.write(
                            "Taxon "+str(taxid)+" not found, skipping "+pdb);
                        continue;
                    taxon = taxa[str(ss['taxon_id'].iloc[0])];
                    struct, created = Structure.objects.get_or_create(
                        pdb_id      = pdb,
                        taxon       = taxon,
                    );
                    if created==False:
                        raise Exception(str(struct)+" exists");
                    for c in ss['chain'].unique():
                        self.stdout.write(pdb+"."+c);
                        sss = ss[ss['chain']==c];
                        if len(sss['protein'].unique())!=1:
                            raise Exception(
                                "Multiple proteins defined for "+pdb+"."+chain
                            );
                        protein = None;
                        if sss['protein'].iloc[0] in prots:
                            protein = prots[sss['protein'].iloc[0]];
                        schain, created = StructureChain.objects.get_or_create(
                            structure = struct,
                            protein = protein,
                            name = c,
                        );
                        if created==False:
                            raise Exception(pdb+"."+chain+" exists");
        except: raise;
