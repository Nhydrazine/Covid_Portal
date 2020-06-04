import sys, time;
import numpy as np, pandas as pd;
import urllib, requests, xmltodict, pprint;
################################################################################
txidfile = "../taxon/taxonomy_parsed.csv"; # taxon ID file
outfile = "./fetched_proteins.fna"; # GB records for all proteins fetched
failfile = "./failed_fetch_taxa.csv"; # taxon_ids whose protein fetch failed
################################################################################
def fetch_protein_ids_from_taxon_id(taxon_id, protein_name="spike"):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?";
    options = {
        'term'          : "txid"+taxon_id+"[Oraganism:noexp] AND "+protein_name,
        'db'            : "protein",
        'usehistory'    : "n",
    }
    url = base + urllib.parse.urlencode(options);
    r = xmltodict.parse(requests.get(url).text);
    try: returnval = r['eSearchResult']['IdList']['Id'];
    except: return None;
    if type(returnval)==list: return returnval;
    else: return [returnval];

def fetch_protein_gbs_from_taxon_id(taxon_id, protein_name="spike", retmax=500):
    base_search = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?";
    base_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?";
    search_options = {
        'term'          : "txid"+taxon_id+"[Oraganism:noexp] AND "+protein_name,
        'db'            : "protein",
        'usehistory'    : "y",
    };

    url = base_search + urllib.parse.urlencode(search_options);
    r = xmltodict.parse(requests.get(url).text)['eSearchResult'];

    buffer = [];
    if int(r['Count'])>0:
        for restart in range(0,int(r['Count']),retmax):
            fetch_options = {
                'db'        : 'protein',
                'WebEnv'    : r['WebEnv'],
                'query_key' : r['QueryKey'],
                'retmax'    : str(retmax),
                'rettype'   : 'gb',
                'retmode'   : 'text',
            }
            fetch_url = base_fetch + urllib.parse.urlencode(fetch_options);
            gbs = requests.get(fetch_url).text;
            buffer.append(gbs);
    return buffer;


################################################################################
failed_ids = [];
df = pd.read_csv(txidfile);
taxon_ids = df['gb_taxon_id'][
    (df['leaf']==True) &
    (df['pcount']>0)
].astype(str);

fh = open(outfile, "w");
for taxon_id in taxon_ids:
    print("Downloading for "+taxon_id+" ... ", end='', flush=True);
    try:
        gbs = fetch_protein_gbs_from_taxon_id(taxon_id);
        print("OK");
        fh.write("".join(gbs));
    except:
        print("Failed "+taxon_id);
        failed_ids.append(taxon_id);
        fh.close();
        sys.exit();
    time.sleep(1);
fh.close();
print("Wrote to "+outfile);
failed_ids = pd.DataFrame({'taxon_id': failed_ids});
print("Writing "+failfile);
failed_ids.to_csv(failfile);
