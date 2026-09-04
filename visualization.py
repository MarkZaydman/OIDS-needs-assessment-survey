"""

visualization.py

Mark Zaydman
20260904

Purpose: Visualize OIDS Needs Assessment Survey Data

"""

#%% imports
# standard library

# third party
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# local

#%% functions
def import_data(fpath:str='2026_OIDS_Needs_Assessment_Survey_Draft.csv') -> 'pd.DataFrame':
    """
    Import OIDS Needs Assessment Survey Data from CSV file

    Parameters
    ----------
    fpath : str, optional
        Path to the CSV file. The default is '2026_OIDS_Needs_Assessment_Survey_Draft.csv'.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the survey data.

    """
    import pandas as pd

    # Read the CSV file into a DataFrame
    df = pd.read_csv(fpath)

    return df
# %%
def main() -> pd.DataFrame:
    """
    Main function to import and visualize OIDS Needs Assessment Survey Data.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the survey data.

    """
    # Import the survey data
    df = import_data()

    # Display the first few rows of the DataFrame
    print(df.head())

    return df

if __name__ == "__main__":
    df = main()
# %%


# %%
