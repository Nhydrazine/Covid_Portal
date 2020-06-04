from django.db import models
################################################################################
# PROTEINS AND TAXA
################################################################################
class Taxon(models.Model):
    """NCBI Taxon object model.

    Attributes
    ----------
    gb_taxon_id : str
        GenBank Taxon ID, unique.
    leaf : boolean
        Is this taxon a leaf (True) or a node (False)?
    path : str
        Period-separated list of ancestral gb_taxon_id starting
        with the farthest ancestor (left) to the nearest (right).
    name : str
        Name of the taxon.
    level : str
        Level (Genus, Family etc...)

    """
    gb_taxon_id = models.CharField(max_length=20, unique=True);
    leaf = models.BooleanField();
    path = models.CharField(max_length=200);
    name = models.CharField(max_length=200, unique=True);
    level = models.CharField(max_length=50);
    def __str__(self): return self.name;

class Protein(models.Model):
    """Protein object model.

    Attributes
    ----------
    name : str
        Common name of the protein (unique).
    mesh_id : str
        NCBI MeSH ID of protein for standardization (unique).

    """
    name = models.CharField(max_length=200, unique=True);
    mesh_id = models.CharField(max_length=200, unique=True);
    def __str__(self): return self.name;
################################################################################
# PROTEIN SEQUENCES AND ALIGNMENTS
################################################################################
class Alignment(models.Model):
    """Protein sequence alignment object model. An alignment is a common
    positioning of amino acids among a group of protein sequences.

    Attributes
    ----------
    name : str
        The name of the alignment (unique).
    protein : explorer.models.Protein
        The protein that this alignment applies to.
    date_created : date
        The date the alignment was imported.

    """
    name = models.CharField(max_length=100, unique=True);
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE);
    date_created = models.DateField(auto_now_add=True);
    def __str__(self): return self.name;

class SequenceRecord(models.Model):
    """A SequenceRecord contains meta/desriptive data about a sequence. Note
    that these sequences are assumed to be protein sequences. Nucleotide
    sequences will be added in a later version.

    Attributes
    ----------
    protein : explorer.models.Protein
        Protein to which the sequence record refers.
    taxon : explorer.models.Taxon
        Taxon that is the parent of the sequence or the sequence itself.
    accession : str
        NCBI Accession number (includes version e.g. XXXXX.#) (unique).
    organism : str
        Name of the organism for this sequence.
    collection_date : date
        Date the sequence was obtained (null).
    country : str
        Country or country:region the sequence was obtained from (null).
    host : str
        For pathogens, name of the host that this organism was obtained
        from (null).
    isolation_source : str
        Name of the tissue the sequence was obtained from (null).
    isolate : str
        Name of the viral isolate this sequence refers to.
    coded_by : str
        NCBI Nucleotide sequence region and accession number that codes
        for this protein sequence.

    """
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE);
    taxon = models.ForeignKey(Taxon, on_delete=models.CASCADE);
    accession = models.CharField(max_length=50,unique=True);
    organism = models.CharField(max_length=200);
    collection_date = models.DateTimeField(null=True);
    country = models.CharField(max_length=100, null=True);
    host = models.CharField(max_length=100, null=True);
    isolation_source = models.CharField(max_length=100, null=True);
    isolate = models.CharField(max_length=100, null=True);
    coded_by = models.CharField(max_length=50, null=True);
    def __str__(self): return self.accession;

class Sequence(models.Model):
    """An aligned protein sequence (dash are inserts/gaps).

    Attributes
    ----------
    sequence_record : explorer.models.SequenceRecord
        SequenceRecord that this sequence refers to.
    alignment : explorer.models.Alignment
        Sequence alignment that this sequence belongs to (different
        alignments may not be compatible).
    sequence : str
        Actual sequence, with leading gaps trimmed off.
    offset : int
        How many leading gaps were trimmed? need to be added back to match
        its alignment.

    """
    sequence_record = models.ForeignKey(SequenceRecord, on_delete=models.CASCADE);
    alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE);
    sequence = models.TextField();
    offset = models.IntegerField();
    def __str__(self): return self.sequence;
################################################################################
# POSITION NOMENCLATURES
################################################################################
class Nomenclature(models.Model):
    """An alignment position nomenclature based on a reference sequence. A nomenclature has "major" positions for each non-gap letter in the reference sequence and "minor" positions for each gap letter in the reference sequence. For example:

    ABCDEFGH-IJK--LMNOP---QRSTUVWXYZ (REFERENCE SEQUENCE ALIGNMENT)
    01234567789000123455556789012345 (MAJOR ONES POSITIONS)
    00000000100012000001230000000000 (MINOR ONES POSITIONS)

    The nomenclature references the explorer.models.Sequence that was used
    as a reference. This parent object contains the alignment. The reference Sequence object is also a child of a SequenceRecord which contains the explorer.models.Protein that the nomenclature belongs to. For reference, Django traverses this tree like so:

    > Nomenclature.objects.filter(
    >   sequence__sequence_record__protein__mesh_id = "your mesh id"
    >   sequence__alignemnt = "your alignment"
    > );

    Attributes
    ----------
    name : str
        A name for the nomenclature.
    date_created : date
        The date the nomenclature was inserted into database.
    reference : explorer.models.Sequence
        The reference sequence that the nomenclature is built from.

    """
    name = models.CharField(max_length=100, unique=True);
    date_created = models.DateField(auto_now_add=True);
    reference = models.ForeignKey(Sequence, on_delete=models.CASCADE);
    # alignment is accessed via self.reference.alignment
    # protein is accessed via self.reference.sequence_records.protein
    def __str__(self): return self.name;

class NomenclaturePosition(models.Model):
    """Position indices for an explorer.models.Nomenclature object. There are both "major" and "minor" positions based on the reference sequence and alignment that was chosen for the nomenclature.

    Attributes
    ----------
    index : int
        Index position in the sequence alignment (sequential, no major/minor,
        this should reference the character position in a raw sequence string
        using that alignment).
    nomenclature : explorer.models.Nomenclature
        Nomenclature that this position belongs to.
    major : int
        Major position. Note that 0 indicates positions that are before the first non-gap character of the reference.
    minor : int
        Minor position starting at 0.

    """
    index = models.IntegerField();
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE);
    major = models.IntegerField(); # major position relative to reference
    minor = models.IntegerField(); # minor (or insert) relative to reference
    def __str__(self): return str(self.major)+'.'+str(self.minor).rjust(3,'0');
################################################################################
# EPITOPES
################################################################################
class Epitope(models.Model):
    """B/T-cell epitope sequence from ViPR/IEDB.

    Attributes
    ----------
    IEDB_ID : char
        IEDB ID for the epitope sequence.
    protein : explorer.models.Protein
        Protein that this epitope sequence is for. Note that one protein per
        epitope does not reflect the biological reality of epitopes. We can
        develop a more sophistocated approach later.
    alignment : explorer.models.Alignment
        Alignment that this eptiope was matched to, so that it lines up with
        the correct amino acid positions.
    sequence : str
        Aligned sequence of the epitope with leading and trailing gaps
        deleted.
    offset : int
        How many leading gaps were trimmed? need to be added back to match
        its alignment (see explorer.models.Sequence).

    """
    IEDB_ID = models.CharField(max_length=50);
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE);
    alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE);
    sequence = models.TextField();
    offset = models.IntegerField();
    def __str__(self):
        return self.sequence;

class EpitopeExperiment(models.Model):
    """Experimental results of an epitope. Note that from IEDB/ViPR there were many duplicates with the same values for all attributes. All duplicates were removed on import. A more sophistocated system will be needed to include replicates like that, and unique identifying features should be explored for those.

    Attributes
    ----------
    epitope : explorer.models.Epitope
        The epitope that this experiment used.
    host : str
        The name of the host organism used for the experiment.
    assay_type : str
        Name of the assay type (e.g. "ELISA").
    assay_result : str
        Result of the assay (single-word categorical description).
    mhc_allele : str
        Four-digit resolved HLA recognizing the epitope.
    mhc_class : str
        MHC class tested (I is T cell, II is B cell).
    exp_method : str
        Experimental method used (subclass of assay type).
    measurement_type : str
        Type of measurement (binding, lysis activity etc...).

    """
    epitope = models.ForeignKey(Epitope, on_delete=models.CASCADE);
    host = models.CharField(max_length=75);
    assay_type = models.CharField(max_length=50);
    assay_result = models.CharField(max_length=50);
    mhc_allele = models.CharField(max_length=30);
    mhc_class = models.CharField(max_length=30);
    exp_method = models.CharField(max_length=100);
    measurement_type = models.CharField(max_length=100);
    def __str__(self):
        return '_'.join([
            self.epitope.IEDB_ID,
            self.host.replace(' ','-'),
            self.assay_type.replace(' ','-'),
        ]);
        # # DEBUG
        # return '_\n\t'.join([
        #     self.epitope.IEDB_ID,
        #     self.host.replace(' ','-'),
        #     self.assay_type.replace(' ','-'),
        #     self.assay_result.replace(' ','-'),
        #     "MHC-"+self.mhc_allele.replace(' ','-'),
        #     self.mhc_class.replace(' ','-'),
        #     self.exp_method.replace(' ','-'),
        #     self.measurement_type.replace(' ','-')
        #
        # ]);
################################################################################
# CRYSTAL STRUCTURES
################################################################################
class Structure(models.Model):
    pdb_id = models.CharField(max_length=10);
    taxon = models.ForeignKey(Taxon, on_delete=models.CASCADE);

class StructureChain(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE);
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE);
    name = models.CharField(max_length=1);

class StructureChainSequence(models.Model):
    chain = models.ForeignKey(StructureChain, on_delete=models.CASCADE);
    alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE);
    offset = models.IntegerField();
    sequence = models.TextField();

class StructureChainAtom(models.Model):
    chain = models.ForeignKey(StructureChain, on_delete=models.CASCADE);
    resix = models.IntegerField(); # index relative to RAW ungapped sequence
    resid = models.IntegerField(); # index specified in crystal structure
    resn = models.CharField(max_length=1); # single-letter amino acid code
    atom = models.CharField(max_length=5);
    element = models.CharField(max_length=5);
    charge = models.IntegerField();
    occupancy = models.FloatField();
    x = models.FloatField();
    y = models.FloatField();
    z = models.FloatField();




# fin.
