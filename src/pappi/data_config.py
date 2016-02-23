"""
Defines the file paths for all data files
"""

# for getting the current file path
import os
# for getting all PSICQUIC files
import re

# go two folders up
cur_folder = os.path.dirname(__file__)
base_folder = os.path.join(cur_folder, '..', '..')

EXT_DATA_FOLDER = os.path.join(base_folder, '..', 'data')
DATA_FOLDER = os.path.join(base_folder, 'data')

PPI_DATA_FOLDER = os.path.join(DATA_FOLDER, 'ppis')
EXPR_DATA_FOLDER = os.path.join(DATA_FOLDER, 'expr')
GO_DATA_FOLDER = os.path.join(DATA_FOLDER, 'go')
MAP_DATA_FOLDER = os.path.join(DATA_FOLDER, 'mapping')

# TODO add these files into the repo data folder !?
DATABASE = os.path.join(DATA_FOLDER, 'sql_database.sqlite')

# mapping
HGNC_FILE = os.path.join(MAP_DATA_FOLDER, 'hgnc_downloads.txt')
BIOMART_FILE = os.path.join(MAP_DATA_FOLDER, 'mart_export.csv')

# Gene Atlas mapping
GNF1H_ANNOT_FILE = os.path.join(EXPR_DATA_FOLDER, 'gnf1h.annot2007.tsv')
U133A_ANNOT_FILE = os.path.join(EXPR_DATA_FOLDER, 'GPL96-15653.txt')

# paths to PPIs
CCSB_FILE = os.path.join(PPI_DATA_FOLDER, 'HI-II-14.tsv')
CCSB_SEC_FILE = os.path.join(PPI_DATA_FOLDER, 'hppi_sec.txt')
BOSSI_FILE = os.path.join(PPI_DATA_FOLDER, 'CRG.integrated.human.interactome.txt')
HAVU_FILE = os.path.join(PPI_DATA_FOLDER, 'cell_havugimana_ppi.tsv')
STRING_FILE = os.path.join(PPI_DATA_FOLDER, 'protein.links.v10.500.txt')

# PSICQUIC PPIs:
PSICQUIC_FILES = [os.path.join(PPI_DATA_FOLDER, f)
                  for f in os.listdir(PPI_DATA_FOLDER)
                  if re.search('PSICQUIC', f)]


# import expression data sets
HPA_FILE = os.path.join(EXPR_DATA_FOLDER, 'normal_tissue.csv')
HPARNA_FILE = os.path.join(EXPR_DATA_FOLDER, 'rna_tissue.txt')
EMTAB_FILE = os.path.join(EXPR_DATA_FOLDER, 'E-MTAB-513.tsv')
RNASEQ_ATLAS_FILE = os.path.join(EXPR_DATA_FOLDER, 'RNA_Seq_Atlas_rev1.txt')
GENE_ATLAS_FILE = os.path.join(EXPR_DATA_FOLDER, 'U133AGNF1B.gcrma.avg.csv')

# GO terms:
GO_OBO_FILE = os.path.join(GO_DATA_FOLDER, 'gene_ontology.1_2.obo')
GO_ASSOC_FILE = os.path.join(GO_DATA_FOLDER, 'gene_association.goa_ref_human')

# GO scoring generated files
GO_SCORE_FILE = os.path.join(GO_DATA_FOLDER, 'simrel_scoring.npy')
GO_SCORE_MAP_FILE = os.path.join(GO_DATA_FOLDER, 'score_mapping.json')
GO_BPSCORE_FILE = os.path.join(GO_DATA_FOLDER, 'bp_score.npy')
GO_BPSCORE_ROW_FILE = os.path.join(GO_DATA_FOLDER, 'row_sums.npy')
GO_BPSCORE_MAP_FILE = os.path.join(GO_DATA_FOLDER, 'gene_bpscore_mapping.json')
