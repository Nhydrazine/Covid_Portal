import os, sys, numpy as np, pandas as pd;
from django.core.management.base import BaseCommand, CommandError;
from django.db import models, transaction, IntegrityError;
from django.db.models import Value as V, CharField;
from django.db.models.functions import Concat, Cast;
from explorer.models import Structure, StructureChain, StructureChainResidue, StructureAtom;
################################################################################
# NOTE TODO: This would be way more efficient as follows:
#   1. use django's "bulk create" for residues
#   2. select the residue objects and use those in arguments for bulk create
#      for atoms.
################################################################################
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, nargs='+');

    def handle(self, *args, **options):

        # field list
        fields = {
            'pdb_id'        : str,
            'chain'         : str,
            'resix'         : int,
            'resid'         : int,
            'resn'          : str,
            'atom'          : str,
            'element'       : str,
            'charge'        : int,
            'occupancy'     : float,
            'x'             : float,
            'y'             : float,
            'z'             : float,
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

        # get chains.
        chains = {};
        for c in StructureChain.objects.annotate(
            pdb_chain=Concat('structure__pdb_id', V('.'), 'name')
        ).filter(
            pdb_chain__in=(records['_pdb_chain'])
        ):
            chains[c.pdb_chain] = c;

        # trim all records whose pdb_chain wasn't found
        records = records[records['_pdb_chain'].isin( chains.keys() )];
        records['_pcrix'] = \
        records['_pdb_chain']+"@"+records['resix'].astype(str);

        try:
            with transaction.atomic():
                # create residue records using bulk_create
                # subset residues only
                resrecs = records.drop_duplicates(
                    subset=['_pdb_chain','resix'],
                    keep='first');
                # build objects to insert
                print("Building and inserting "+str(len(resrecs))+" residues...");
                StructureChainResidue.objects.bulk_create(
                    (
                        StructureChainResidue(
                            chain   = chains[ r['_pdb_chain'] ],
                            resix   = r['resix'],
                            resid   = r['resid'],
                            resn    = r['resn'],
                        ) for i,r in resrecs.iterrows()
                    )
                );

                # retrieve objects with IDs, by PDB/chain
                for pc in records['_pdb_chain'].unique():
                    ss = records[records['_pdb_chain']==pc];
                    # get residue objects
                    residues = {};
                    for residue in StructureChainResidue.objects.annotate(
                        pdb_chain=Concat(
                            'chain__structure__pdb_id',
                            V('.'),
                            'chain__name'
                        )
                    ).filter(
                        pdb_chain__in=(ss['_pdb_chain'])
                    ):
                        residues[
                            residue.chain.structure.pdb_id+"."+
                            residue.chain.name+"@"+
                            str(residue.resix)
                        ] = residue;

                    # build/insert objects
                    print(
                        "Buildling/inserting for "+str(len(ss))+" atoms for "+pc+"...");
                    StructureAtom.objects.bulk_create(
                        (
                            StructureAtom(
                                residue     = residues[ r['_pcrix'] ],
                                atom        = r['atom'],
                                element     = r['element'],
                                charge      = r['charge'],
                                occupancy   = r['occupancy'],
                                x           = r['x'],
                                y           = r['y'],
                                z           = r['z'],
                            ) for i,r in ss.iterrows()
                        )
                    );
        except: raise;
        return;
