import numpy as np, pandas as pd;
import re;
################################################################################
# Taxonomy Parser
# ---------------------------------------------------------------------------- #
# Parses NCBI taxonomy search output into csv family tree file that contains
# information and links about individual taxa and their 'path' in the tree.
################################################################################
infile = "taxonomy_results_20200515.html"; #
outfile = "taxonomy_parsed.csv";  #csv output file
################################################################################
def parseline(line):
    """Parses a single NCBI taxonomy webpage line, extracting relevant
    information using regex.

    Parameters
    ----------
    line : str
        The line to be parsed (stripping not required).

    Returns
    -------
    dict
        A dictionary of extracted information with the following keys:
            path : str
                A '.' separated list of taxon ids that are parents of the
                current taxon item.
            taxon_id : str
                The taxon id of the current item.
            name : str
                The name of the current item.
            type : str
                The list bullet type, used for debug.
            href : str
                Link to the taxon item's page.
            plink : str
                Link to the taxon item's protein list page.
            pcount : int
                Number of proteins listed (all protein, not just S) for the
                taxon item.

    """
    # for taxon info excluding ID
    rxes_taxon = [
        '\<LI TYPE\=(?P<type>\w+?)\>',
        '\<A TITLE\=\"(?P<title>[\w,\s]+?)\" HREF\=\"(?P<href>.*?)\"\>',
        '.*?\<STRONG\>(?P<name>.+?)\<\/STRONG\>\<\/A\>',
    ];
    # for taxon ID only
    rxes_taxonid = [
        'id\=(?P<taxon_id>\d+?)\&',
    ];
    # for protein info
    rxes_protein = [
        '\<A TITLE=\"Protein\" HREF=\"(?P<plink>.*?)\"\>',
        '\<SPAN.*?\>(?P<pcount>[0-9,\,]+?)\<\/SPAN\>',
    ];
    m = re.search(''.join(rxes_taxon),line);
    if not m: return None;
    taxon = m.groupdict();

    m = re.search(''.join(rxes_taxonid),taxon['href']);
    if not m: return None;
    taxonid = m.groupdict();

    m = re.search(''.join(rxes_protein),line);
    if not m: protein = { 'plink': None, 'pcount': 0 };
    else: protein = m.groupdict();

    return {**taxon, **protein, **taxonid};
################################################################################
# Load file and parse, track branch "paths" as you go, and counting children
# for each so we can designate as node or leaf.
buffer = [];
with open(infile, 'r') as fh:
    buffer = fh.readlines();

extracted = [];
path = [];
new_branch = False;
end_branch = False;
previous_taxon_id = '0';
child_count = { '0' : 0 };
for l in buffer:
    if l.strip()=="<UL COMPACT>":
        new_branch = True;
        continue;
    elif l.strip()=="</UL>":
        end_branch = True;
        continue;
    else:
        edict = parseline(l);
        if not edict:
            # print(("Couldn't parse line :" + l).strip());
            continue;
        if new_branch == True:
            path.append(previous_taxon_id);
            child_count[previous_taxon_id] = 0;
            new_branch = False;
        if end_branch == True:
            parent = path.pop();
            end_branch = False;
        child_count[path[-1]]+=1;
        extracted.append({
            **{
                'path': '.'.join(path),
                'leaf': '', #set after taxonomy is processed
            },
            **edict
        });
        previous_taxon_id = edict['taxon_id'];

# Designate leaf and node using child counts
parent_ids = list(child_count.keys());
for i in range(0,len(extracted)):
    taxon_id = extracted[i]['taxon_id'];
    if taxon_id in parent_ids:
        extracted[i]['leaf'] = False;
    else:
        extracted[i]['leaf'] = True;

################################################################################
# Convert to dataframe and store
df = pd.DataFrame(extracted);
print("Extracted "+str(len(df))+" entries.");
df['pcount'] = df['pcount'].replace(',','',regex=True).astype(int);
df['gb_taxon_id'] = df['taxon_id'];
df['level'] = df['title'];
cols = ['leaf','path','gb_taxon_id','name','level','type','href','plink','pcount'];

df[cols].to_csv(outfile, header=True, index=False);
