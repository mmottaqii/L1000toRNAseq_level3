# Single Cell RNA-seq Data Preprocessing

This repository contains Jupyter notebooks used for the preprocessing of single-cell RNA-seq datasets. The preprocessing steps include data cleaning, normalization, comparative analysis, and data preparation to ensure the quality and usability of the data for further analysis.

## Project Overview

The aim of this project is to systematically prepare single cell RNA-seq data by applying various preprocessing steps, ensuring that the data is primed for high-quality downstream analyses.

### Source Data

The original datasets used in this project can be accessed [here](https://maayanlab.cloud/sigcom-lincs/#/Download).

## Repository Structure

- `assets/`: Contains graphical assets and additional resources used in the notebooks.
- `scripts/`: Contains Jupyter notebooks for data preprocessing:
  - `preprocessing_1.ipynb`: Handles initial data loading, cleaning, and basic statistical analysis.
  - `Preprocessing_2.ipynb`: Further cleans the data, subsets it for analysis, and exports it for use in downstream applications.
  - `rank_value.ipynb`: Performs comparative analysis, data manipulation, and final data preparation.
- `README.md`: This file, describing the project and repository structure.

## Key Notebooks

- **preprocessing_1.ipynb**: Starts with data loading, followed by initial cleaning and basic statistical analysis.
- **Preprocessing_2.ipynb**: Focuses on further data cleaning, subsetting, and exporting the data for downstream uses.
- **rank_value.ipynb**: Handles complex data manipulations, comparative analyses, and prepares final datasets for analysis.

## How to Use

1. Clone this repository to your local machine.
2. Ensure you have Jupyter Notebook or JupyterLab installed.
3. Navigate to the `scripts/` directory and open the notebooks using Jupyter.
4. Run the notebooks in sequence to replicate the preprocessing steps.

## Dependencies

- Python 3
- Pandas
- Numpy
- Matplotlib
- h5py
- Other Python libraries as required for data handling and visualization.

## Contact

For any further inquiries or contributions, feel free to contact the repository maintainer.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/blob/main/LICENSE) file for details.
