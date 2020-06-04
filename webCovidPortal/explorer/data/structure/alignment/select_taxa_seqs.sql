
select
    t.gb_taxon_id as taxon_id,
    t.name,
    t.leaf,
    sr.organism,
    sr.isolate,
    sr.accession,
    aln.name as alignment,
    s.sequence,
    s.offset
from explorer_taxon as t
join explorer_sequencerecord as sr on sr.taxon_id==t.id
join explorer_sequence as s on s.sequence_record_id=sr.id
join explorer_alignment as aln on aln.id = s.alignment_id
where t.gb_taxon_id in (277944,227859,443239,1335626,228407,11137,1263720,11120,1235996,2697049)
and explorer_alignment.name = "20200505"
