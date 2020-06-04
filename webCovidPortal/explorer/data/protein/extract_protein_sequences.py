import sys, re;
import numpy as np, pandas as pd;
from Bio import SeqIO;
import pprint;
################################################################################
# infile = "test_gbs.fna";
infile = "fetched_proteins.fna";
outfile = "gb_extract.csv";
################################################################################
pp = pprint.PrettyPrinter(indent=4);
################################################################################
rows = {};
print("Loading "+infile);
# These were not caught by prior filters
invalids = [
    'ACN89771.1',   # MHV orf1b
    'ACN89724.1',   # MHV orf1b
    'ACN89691.1',   # MHV orf1b
    'ACN89704.1',   # MHV orf1b
    'ACO72891.1',   # MHV orf1b
    'ACO72882.1',   # MHV orf1b
    'P0C6X9.1',     # MHV orf1a
    'ACN89769.1',   # MHV orf1a
    'ACN89729.1',   # MHV orf1a
    'ACN89685.1',   # MHV orf1a
    'ACN89709.1',   # MHV orf1a
    'P0C6V0.1',     # MHV orf1a
    'ACO72890.1',   # MHV orf1a
    'AC072881.1',   # removed at submitter's request
    'QJE50588.1',   # SARS Urbani orf1a
    'QJE50587.1',   # SARS Urbani orf1ab
    'ACO72881.1',   # MHC orf1a
    'Q66165.2', 'Q9QAR6.1', 'P31613.1', 'P69609.1', 'P22052.1', 'P15779.1',
    'P15778.1', 'P15776.1', 'P33468.1', 'P59710.1', 'Q9QAQ9.1', 'Q9DR81.1',
    'P59709.1', 'P59711.1', 'Q8V437.1', 'P30215.1', '5N11_B.1', '5N11_A.1',
    'Q8BB26.1', 'Q8JSP9.1', 'Q5MQD1.1', 'Q14EB1.1', 'Q0ZME8.1', 'ACN89770.1',
    'ACN89768.1', 'ACN89767.1', 'ACN89766.1', 'ACN89765.1', 'ACN89764.1',
    'ACN89762.1', 'ACN89761.1', 'ACN89692.1', 'ACN89690.1', 'ACN89688.1',
    'ACN89687.1', 'ACN89686.1', 'ACN89684.1', 'ACN89711.1', 'ACN89710.1',
    'ACN89708.1', 'ACN89707.1', 'ACN89706.1', 'ACN89733.1', 'ACN89732.1',
    'ACN89731.1', 'ACN89730.1', 'ACN89728.1', 'ACN89727.1', 'ACN89726.1',
    'ACN89725.1', 'O92367.1',
    'AAB19590.1', 'P69614.2', 'P0C5A8.1', 'P0C5A7.1', 'P0C2R0.1',
    'P03416.2', 'P31615.2', 'P19738.1', 'P03415.1', '1WDG_B.1', '1WDG_A.1',
    '1WDF_B.1', '1WDF_A.1', 'ACO72898.1', 'ACO72897.1', 'ACO72896.1',
    'ACO72895.1', 'ACO72894.1', 'ACO72892.1', 'ACO72889.1', 'ACO72888.1',
    'ACO72887.1', 'ACO72885.1', 'ACO72883.1', 'Q83356.1', 'P31614.2',
    'O91262.1',
    'Q9IKD2.1', 'YP_009072439.1','AIL94215.1', 'ADY17911.1', 'Q0Q470.1', 'Q3I5J0.1',
    'AAP94737.1', 'AAP94748.1', 'AAP94759.1', 'AAP30713.1', 'AAP13567.1',
    'AAT52330.1', 'AAR14803.1', 'AAR14807.1', 'AAR14811.1', '2OFZ_A.1',
    '2OG3_A.1', 'AAP37017.1', 'AAR87501.1', 'AAR87512.1', 'AAR87523.1',
    'AAR87534.1', 'AAR87545.1', 'AAR87556.1', 'AAR87567.1', 'AAR87578.1',
    'AAR87589.1', 'AAR87600.1', 'QJE50600.1', 'QJE50599.1', 'QJE50598.1',
    'QJE50597.1', 'QJE50596.1', 'QJE50595.1', 'QJE50594.1', 'QJE50593.1',
    'QJE50592.1', 'QJE50591.1', 'QJE50590.1', 'CAL40866.1', 'P0DTC7.1',
    '1ZV7_A.1', '1ZV7_B.1', '3JCL_A.1', '3JCL_B.1', '3JCL_C.1', '4KQZ_A.1',
    '4KQZ_B.1', '4KR0_B.1', '4L3N_A.1', '4L3N_B.1', '4MOD_A.1', '4MOD_B.1',
    '4XAK_A.1', '4XAK_B.1', '4ZPT_R.1', '4ZPT_S.1', '4ZPV_R.1', '4ZPV_S.1',
    '4ZPW_R.1', '4ZPW_S.1', '5GNB_A.1', '5I08_A.1', '5I08_B.1', '5I08_C.1',
    '5KWB_A.1', '5X58_A.1', '5X58_B.1', '5X58_C.1', '5X5B_A.1', '5X5B_B.1',
    '5X5B_C.1', '6B3O_A.1', '6B3O_B.1', '6B3O_C.1', '6C6Y_R.1', '6C6Y_S.1',
    '6JHY_A.1', '6LVN_A.1', '6LVN_B.1', '6LVN_C.1', '6LVN_D.1', '6LXT_A.1',
    '6LXT_B.1', '6LXT_C.1', '6LXT_D.1', '6LXT_E.1', '6LXT_F.1', '6LZG_B.1',
    '6M0J_E.1', '6M17_E.1', '6M17_F.1', '6NZK_A.1', '6NZK_B.1', '6NZK_C.1',
    '6OHW_A.1', '6OHW_B.1', '6OHW_C.1', '6Q04_A.1', '6Q04_B.1', '6Q04_C.1',
    '6Q05_A.1', '6Q05_B.1', '6Q05_C.1', '6Q06_A.1', '6Q06_B.1', '6Q06_C.1',
    '6Q07_A.1', '6Q07_B.1', '6Q07_C.1', '6VSB_A.1', '6VSB_B.1', '6VSB_C.1',
    '6VSJ_A.1', '6VSJ_B.1', '6VSJ_C.1', '6VXX_A.1', '6VXX_B.1', '6VXX_C.1',
    '6VYB_A.1', '6VYB_B.1', '6VYB_C.1', '6W41_C.1', '6YLA_A.1', '6YLA_E.1',
    '6YM0_E.1', '6YOR_A.1', '6YOR_E.1', '7BZ5_A.1',
];
for record in SeqIO.parse(infile,"genbank"):
    row = {};
    row['taxon_id'] = "";
    row['description'] = record.description;
    row['accession'] = record.annotations['accessions'][0];
    row['organism'] = record.annotations['organism'];
    version = (
        row['accession']+"."+
        str(record.annotations.get('sequence_version',"1"))
    );
    if version in invalids:
        continue; # skip
    row['version'] = version;
    row['seq'] = str(record.seq);

    if version in rows:
        # compare sequences
        if row['seq']!=rows[version]['seq']:
            raise Exception("Distinct sequences for version "+version);
        else:
            print("\t"+row['organism']+" ... SKIP");
            continue; #skip to next

    print("\t"+row['organism']+" ... ",end="", flush=True);
    row['references'] = [];
    for r in record.annotations['references']:
        if r.pubmed_id!="":
            row['references'].append(r.pubmed_id);

    def dgf(d, k):
        return d.get(k, [""])[0];

    record_cds = 0;
    for f in record.features:
        if f.type=="source":
            d = f.qualifiers;
            row['collection_date'] = dgf(d, "collection_date");
            row['country'] = dgf(d, "country");
            row['host'] = dgf(d, "host");
            row['isolation_source'] = dgf(d, "isolation_source");
            if "strain" in d:
                row['isolate'] = dgf(d, "strain");
            elif "isolate" in d:
                row['isolate'] = dgf(d, "isolate");
            else:
                row['isolate'] = row['organism']
            if "db_xref" in d:
                for ref in d['db_xref']:
                    if ref[0:5]=="taxon":
                        row['taxon_id'] = ref[6:];

        elif f.type=="CDS":
            record_cds+=1;
            if record_cds>1:
                raise Exception("Multiple CDS identified for "+row['organism']);
            d = f.qualifiers;
            row['coded_by'] = dgf(d, "coded_by");

    rows[version] = row;
    print("OK");
print("Concatenating...");
df = pd.DataFrame(rows.values(), index=rows.keys());
print("Checking for duplicate versions...");
if len(list(df['version'].unique())) != len(df):
    print(
        "ERROR: There are "+str(len(list(df['version'].unique())))+
        " unique accession.versions and "+str(len(df))+" total records..."
    );
print("Writing "+outfile);
df.to_csv(outfile);


# Issues to be aware of:
#   1. Strain vs. Isolate in record.features type "source", some have neither.
#       Use strain, then isolate, then organism name in that order.
#   2. Make sure every record has only one or no CDS record
