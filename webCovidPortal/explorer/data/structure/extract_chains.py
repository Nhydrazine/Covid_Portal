import sys, os, re;
import numpy as np, pandas as pd;
################################################################################
source_folder = "./downloads";
outfile = "./chains.csv";
rx_molid = re.compile("^COMPND\s+MOL\_ID\: (\d+)");
rx_molname = re.compile("^COMPND[\s,\d]+MOLECULE: ([A-Z,a-z,0-9,\s]+)");
rx_molchain = re.compile("^COMPND[\s,\d]+CHAIN: ([A-Z,\,,\s]+)");
rx_taxid = re.compile("^SOURCE[\s,\d]+ORGANISM\_TAXID\: ([\d]+?);");
chains = [];
for fn in os.listdir(source_folder):
    if fn.endswith(".pdb"):
        pdb_id = os.path.splitext(fn)[0];
        print(pdb_id+" ... ",end='',flush=True);
        fh = open(source_folder+"/"+fn,'r');
        lines = fh.readlines();
        mol_id = 0;
        mol_name = "";
        mol_chains = [];
        taxon_id = 0;
        for l in lines:
            if l[0:6]=="SOURCE":
                m = re.match(rx_taxid, l);
                if m: taxon_id = int(m.group(1));
            if l[0:6]=="COMPND":
                # assign molecule id where specified
                m = re.match(rx_molid, l);
                if m: mol_id = int(m.group(1));
                # get molecule name where specified
                if mol_id>0:
                    m = re.match(rx_molname, l);
                    if m: mol_name = m.group(1);
                # get chains where specified
                if mol_id>0:
                    m = re.match(rx_molchain, l);
                    if m: mol_chains += m.group(1).replace(' ','').split(',');
            # store if all defined
            if mol_id>0 and mol_name!="" and len(mol_chains)>0 and taxon_id>0:
                for c in mol_chains:
                    row = {
                        'pdb_id'    : pdb_id,
                        'mol_id'    : mol_id,
                        'mol_name'  : mol_name,
                        'chain'     : c,
                        'taxon_id'  : taxon_id,
                    };
                    chains.append(row);
                # reset
                mol_id=0;
                mol_name="";
                mol_chains=[];
                break;
        fh.close();
        print(" OK");
    else: continue;
print("Dataframing...");
df = pd.DataFrame(chains);
print("Writing "+outfile);
df.to_csv(outfile);

# sample compound line(s)
# COMPND    MOL_ID: 1;
# COMPND   2 MOLECULE: SPIKE GLYCOPROTEIN;
# COMPND   3 CHAIN: A, B, C;
# COMPND   4 ENGINEERED: YES
