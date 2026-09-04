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

#%% globals

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

def format_division(df:pd.DataFrame) -> pd.DataFrame:
    """
    Format the 'Q1' column in the DataFrame by replacing division names with abbreviations.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the survey data.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with formatted 'Q1' column.

    """
    map = {
    'Anatomic and Molecular Pathology':'AMP',
    'Immunobiology':'IMM',
        'Laboratory and Genomic Medicine':'LGM',
        'Overall Department (not in a Division)':'Department',
        'Genomic and Molecular Pathology':'GMP',
        'Neuropathology':'NP',
    }
    df['Q1'] = df['Q1'].str.replace(map)
    df['Q1'] = df['Q1'].str.replace(',',' + ')
    return df

def plot_respondents_by_division_role(
    df: pd.DataFrame,
    division_col: str = 'Q1',
    role_col: str = 'Q2',
) -> None:
    """
    Plot number of respondents per division, broken out by primary role.

    Parameters
    ----------
    df : pd.DataFrame
        Survey data.
    division_col : str, optional
        Column containing division, by default 'Q1'.
    role_col : str, optional
        Column containing primary role, by default 'Q2'.

    Returns
    -------
    None
    """

    # Keep respondents with both division and role reported
    df_plot = df[[division_col, role_col]].dropna().copy()

    # Count respondents by division and role
    counts = (
        df_plot
        .groupby([division_col, role_col])
        .size()
        .unstack(fill_value=0)
    )

    # Sort divisions by total number of respondents
    counts = counts.loc[counts.sum(axis=1).sort_values(ascending=True
                                                       ).index]

    # Plot
    fig, ax = plt.subplots(figsize=(7, 3))

    counts.plot(
        kind='barh',
        stacked=True,
        ax=ax,
        color=sns.color_palette("colorblind",n_colors=len(counts.columns)),
        width=0.8
    )

    # Formatting
    ax.set_xlabel('Number of Respondents')
    ax.set_ylabel('Division')
    # ax.set_title('OIDS Needs Assessment Respondents by Division and Primary Role')

    ax.legend(
        title='Primary Role',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        frameon=False,
    )

    # ax.tick_params(axis='x', rotation=45)

    sns.despine()

    fig.tight_layout()
    plt.show()

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
    df = format_division(df)
    plot_respondents_by_division_role(df)
    return df

if __name__ == "__main__":
    df = main()
# %%

