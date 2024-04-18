# With multi processing

import pandas as pd
import numpy as np
import loompy as lp
import os
from multiprocessing import Pool
import logging

# Configure logging
logging.basicConfig(filename='csv_to_loom_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

CHUNK_SIZE = 8000

def process_file_to_loom(csv_file):
    logging.info(f"Starting processing of file {csv_file}")

    try:
        gene_names = None
        all_gene_data = []
        all_col_attrs = {}

        for chunk in pd.read_csv(csv_file, chunksize=CHUNK_SIZE, low_memory=False):
            if gene_names is None:
                gene_names = chunk.columns[13:].astype('str').tolist()
                all_col_attrs = {attr: [] for attr in chunk.columns[:13]}

            cell_attributes_df = chunk.iloc[:, :13]
            gene_expression_df = chunk.iloc[:, 13:].replace([np.nan, np.inf, -np.inf], -1)
            gene_expression_data = gene_expression_df.values.T.astype(float)
            all_gene_data.append(gene_expression_data)

            for attr in cell_attributes_df.columns:
                all_col_attrs[attr].extend(cell_attributes_df[attr].tolist())

        final_gene_data = np.concatenate(all_gene_data, axis=1)

        for attr in all_col_attrs:
            all_col_attrs[attr] = np.array(all_col_attrs[attr])

        row_attrs = {"gene": gene_names}

        loom_file_name = os.path.splitext(os.path.basename(csv_file))[0] + ".loom"
        lp.create(loom_file_name, final_gene_data, row_attrs=row_attrs, col_attrs=all_col_attrs)

        logging.info(f"Successfully processed and saved file {loom_file_name}")

    except Exception as e:
        logging.error(f"Error processing file {csv_file}: {e}")

def main():
    directory = os.getcwd()
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    num_cpus = 3

    with Pool(num_cpus) as pool:
        pool.map(process_file_to_loom, csv_files)

    logging.info("Completed processing all files.")

if __name__ == "__main__":
    main()

