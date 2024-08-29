from cmapPy.pandasGEXpress.parse import parse
import loompy
import numpy as np

input_file = "/home/jrollins/home/data/sigcom-lincs-L1000toRNAseq/Level3_pred_RNA-Seq-like-L1000/ctl_predicted_RNAseq_profiles.gctx"
output_file = "/home/vmottaqi/control_Sigcom/control_L1000toRNAseq_level3_06122023.loom"
chunk_size = 8000  # Adjust based on your system's memory capacity

# Extract gene names (row metadata)
row_metadata_df = parse(input_file, row_meta_only=True)
gene_names = row_metadata_df.index.values

# Get all column IDs
all_columns = parse(input_file, col_meta_only=True).index.tolist()

# Determine number of chunks
num_chunks = len(all_columns) // chunk_size + (1 if len(all_columns) % chunk_size != 0 else 0)

for i in range(num_chunks):
    start_idx = i * chunk_size
    end_idx = min(start_idx + chunk_size, len(all_columns))
    chunk_columns = all_columns[start_idx:end_idx]

    # Load only required columns for this chunk
    chunk_data = parse(input_file, cid=chunk_columns)
    
    # Convert to matrix
    matrix = chunk_data.data_df.values

    # Prepare column attributes
    col_metadata_df = chunk_data.col_metadata_df
    col_attrs = {col: col_metadata_df[col].values for col in ['cell', 'dose', 'pertname', 'timepoint']}

    # Prepare row attributes
    row_attrs = {"gene": gene_names}

    # If the loom file doesn't exist, create it, otherwise append
    if i == 0:
        loompy.create(output_file, matrix, row_attrs, col_attrs)
    else:
        with loompy.connect(output_file) as ds:
            ds.add_columns(matrix, col_attrs)
    print(f"Processed chunk {i + 1} of {num_chunks}")

print("Completed processing all chunks.")

