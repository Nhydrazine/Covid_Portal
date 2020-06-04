import numpy as np, pandas as pd;
import sys, os, time;
import urllib, requests, xmltodict, pprint;
################################################################################
# PDBIDs are currently determined manually, this list is meant to test the input system.
PDB_IDS = [
'6CV0',
'5X5B',
'5X58',
'6U7H',
'2IEQ',
'2GHV',
'5KWB',
'5GNB',
'6ACC',
'6ACD',
'5XLR',
'4ZPW',
'6Q04',
'6Q06',
'6Q05',
'6Q07',
'5WRG',
'5X5C',
'5X5F',
'5X4R',
'5X4S',
'5X59',
'6VYB'
];

download_to = "./downloads";
print("Fetching PDBs...");
for i in PDB_IDS:
    # setup and display
    print("\t"+i+" ... ", end='', flush=True);
    outfile = download_to+"/"+i+".pdb";
    url = ("https://files.rcsb.org/download/"+i+".pdb");
    # skip if file exists
    if os.path.isfile(outfile):
        print("PDB file already exists...");
        continue;
    # fetch and report error if needed
    result = requests.get(url);
    if result.status_code != 200:
        print("Error "+str(result.status_code));
        continue;
    else:
        # write to file
        with open(outfile,'w') as fh:
            fh.write(result.text);
        print(outfile+" OK");
    # respectfully wait between requests
    time.sleep(1);

# Get PDB annotations
# Extract relevant chains
# Get PDB data for all chains
# extract secondary structure for each residue for relevant chains
# extract coordinates of relevant atoms for relevant chains
# Get sequence data for relevant chains
