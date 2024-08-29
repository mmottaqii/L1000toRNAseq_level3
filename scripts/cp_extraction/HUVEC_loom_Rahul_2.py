# A slight modification added (Dec 11)

import pandas as pd
import numpy as np
import loompy as lp

# Define chunk size for reading CSV in chunks
CHUNK_SIZE = 8000

# This will hold gene names (column names from 16 onward)
gene_names = None
all_gene_data = []
all_col_attrs = {}

# Read the CSV file in chunks
for chunk in pd.read_csv('/home/vmottaqi/cp_extraction/HUVEC_sigcom_data_SMILES_12_5_2023.csv', chunksize=CHUNK_SIZE, low_memory=False):

    if gene_names is None:
        gene_names = chunk.columns[13:].astype('str').tolist()
        all_col_attrs = {attr: [] for attr in chunk.columns[:13]}

    # Extract cell attributes
    cell_attributes_df = chunk.iloc[:, :13]
    
    # Extract and process gene expression values
    gene_expression_df = chunk.iloc[:, 13:]
    gene_expression_df = gene_expression_df.replace([np.nan, np.inf, -np.inf], -1)
    gene_expression_data = gene_expression_df.values.T
    gene_expression_data = gene_expression_data.astype(float)

    all_gene_data.append(gene_expression_data)

    # Extract column attributes
    for attr in cell_attributes_df.columns:
        all_col_attrs[attr].extend(cell_attributes_df[attr].tolist())

# Now, concatenate the chunks
final_gene_data = np.concatenate(all_gene_data, axis=1)

# Convert lists in col_attrs to numpy arrays
for attr in all_col_attrs:
    all_col_attrs[attr] = np.array(all_col_attrs[attr])

# Row attributes
row_attrs = {"gene": gene_names}

# Create the .loom file
lp.create('HUVEC_L1000toRNAseq_12_11_2023.loom', final_gene_data, row_attrs=row_attrs, col_attrs=all_col_attrs)

