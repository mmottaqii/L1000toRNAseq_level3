# For venus files

import pandas as pd
import os
from multiprocessing import Pool
import multiprocessing
import logging

def setup_logging():
    # Configure logging
    logging.basicConfig(filename='csv_meta_processing.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(processName)s - %(message)s')


def process_file(file_path):
    setup_logging()  # Set up logging in each subprocess
    logging.info(f"Starting processing of file {file_path}")

    try:
        # Read the BJAB and SMILES files
        DATA = pd.read_csv(file_path, low_memory=False)
        SMILES = pd.read_csv('/home/vmottaqi/cp_extraction/LINCS_small_molecules_7.tsv', sep='\t')

        # Perform a left merge of BJAB and SMILES on 'pertname'
        merged_df = pd.merge(DATA, SMILES, on='pertname', how='left')

        # Insert the merged columns from SMILES after the 5th column of BJAB
        insert_position = 6
        smiles_columns = [col for col in SMILES.columns if col != 'pertname']
        final_columns = DATA.columns[:insert_position].tolist() + smiles_columns + DATA.columns[insert_position:].tolist()
        merged_df = merged_df[final_columns]

        # Extract the first part of the file name (before "_")
        base_name = os.path.basename(file_path)
        new_file_name = base_name.split('_')[0] + ".csv"
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        # Save the merged DataFrame
        merged_df.to_csv(new_file_path, index=False)
        logging.info(f"Successfully processed and saved file {new_file_path}")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")


def main():
    # Directory containing the CSV files
    directory = os.getcwd()
    # List of CSV file paths
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    # Number of CPUs to use
    num_cpus = 3
    # Create a multiprocessing pool and process the files
    with Pool(num_cpus) as pool:
        pool.map(process_file, csv_files)
    logging.info("Completed processing all files.")


if __name__ == "__main__":
    setup_logging()  # Initial logging setup
    main()

