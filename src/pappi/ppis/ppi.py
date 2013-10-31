import csv
from .. import sql
from .. import id_mapping
from ..table_manager import TableManager

# TODO maybe put this into a config file
UNIFYING_ID = "hgnc"


class PPI(TableManager):
    """ An interface to all PPI networks. """

    # default parameters for the raw file
    file_has_header = True
    file_field_seperator = '\t'
    file_quoting = csv.QUOTE_NONE

    def __init__(self, filename, sql_connection, name,
                 gene1_colname, gene2_colname, orig_id):
        """
        Creates a new PPI network. This MUST explicitly be called
        by all subclasses of this class to properly initialize
        all class members.

        Parameters:
            - filename:         Filename of the ppi network file.
            - sql_connection:   SQL connection object for the database,
                                into which the PPI network is to be
                                imported.
            - name:             The name for the PPI network. This is
                                used for example for the names of the
                                SQL tables.
            - gene1_colname:    The name of the column of the first gene
                                of the interaction.
            - gene2_colname:    The name of the column of the second gene
                                of the interaction.
            - orig_id:          The gene identifier type (e.g. 'uniprot',
                                'ensembl', ...) of the gene columns.
        """
        # call constructor of super-class
        TableManager.__init__(self, name, sql_connection)
        # copy references into the new instance
        self.filename = filename
        self.sql_conn = sql_connection
        self.name = name
        self.gene1_colname = gene1_colname
        self.gene2_colname = gene2_colname
        self.orig_id = orig_id

    def init_ppi(self, verbose=False):
        """
        Performs all the steps of initialization of the PPI network
        including loading the raw file into the SQl database,
        filtering the interactions, mapping to a unifying id and
        normalizing the PPI network to a common format.
        """
        if verbose:
            print("Initializing PPI '" + self.name + "'")
            print("    importing raw file")
        self.import_raw_file()
        if verbose:
            print("    filtering PPI")
        self.filter()
        if verbose:
            print("    mapping ids")
        self.id_mapping()
        if verbose:
            print("    normalizing table")
        self.normalize_table()
        if verbose:
            print("    normalizing graph")
        self.normalize_graph()

    def import_raw_file(self):
        """
        Imports a PPI file in csv format into the SQL database.
        """
        table_name = self.next_tmp_table("raw")
        sql.import_csv(self.filename, table_name, self.file_field_seperator,
                       self.file_has_header, csv_quoting=self.file_quoting,
                       sql_conn=self.sql_conn)

    def filter(self):
        """
        Filters the PPI network for interactions with a certain confidence
        level. This is only implemented for some PPIs. E.g. string-db and
        PSICQUIC have these confidence scores by which the interactions can
        be filtered.
        """
        # the interface/base-class does not implement filtering.
        pass

    def id_mapping(self):
        """
        Maps the gene/protein identifiers to a unifying identfier.
        """
        src_table = self.get_cur_tmp_table()
        dst_table = self.next_tmp_table()
        id_mapping.map_identifier(src_table, [self.gene1_colname,
                                  self.gene2_colname], self.orig_id,
                                  dst_table, UNIFYING_ID, self.sql_conn,
                                  verbose=True)

    def normalize_table(self):
        """
        Maps the columns of the original PPI table
        to columns of names: Gene1, Gene2. So that all tables have
        the same format.
        """
        # this happens right after the id mapping, just take the two mapped
        # ID columns and put them into a new table with column names
        # Gene1 and Gene2
        src_table = self.get_cur_tmp_table()
        dst_table = self.next_tmp_table('normalized')
        sqlquery = ('SELECT '
                    '' + self.gene1_colname + ' AS Gene1, '
                    '' + self.gene2_colname + ' AS Gene2 '
                    'FROM ' + src_table)
        sql.new_table_from_query(dst_table, sqlquery, self.sql_conn)

    def normalize_graph(self):
        """
        Normalizes the PPI network by making it undirected with one
        row (i.e. pair of proteins) per edge (no back and forth edges).
        """
        # this works on the normalized columns with
        # the same identifier for all PPIs, thus
        # this method should not be overwritten
        # by subclasses
        src_table = self.get_cur_tmp_table()
        # this is the last step in the PPI pre-processing,
        # thus the result does not get put into a temporary table
        dst_table = self.next_tmp_table("")
        sqlquery = ('SELECT DISTINCT '
                    'CASE WHEN Gene1 > Gene2 '
                    '  THEN Gene2 ELSE Gene1 '
                    'END AS Gene1, '
                    'CASE WHEN Gene1 > Gene2 '
                    '  THEN Gene1 ELSE Gene2 '
                    'END AS Gene2 '
                    'FROM ' + src_table)
        sql.new_table_from_query(dst_table, sqlquery, self.sql_conn)
