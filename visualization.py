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
    # df['Q1'] = df['Q1'].str.replace(',',' + ')
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

    # Split multi-select responses and explode into individual rows
    df_plot[division_col] = df_plot[division_col].str.split(',')

    df_plot = df_plot.explode(division_col)

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
    ax.set_xlabel(f'Number of Respondents (# unique = {df["ResponseId"].nunique()})')
    ax.set_ylabel('Division (multiple allowed)')
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


def format_curr_activities(df: pd.DataFrame, column: str = 'Q3') -> pd.DataFrame:
    """
    Format the current activities column by splitting multi-select responses into individual rows.

    Parameters
    ----------
    df : pd.DataFrame
        Survey data.
    column : str, optional
        Column containing current activities, by default 'Q3'.

    Returns
    -------
    pd.DataFrame
        DataFrame with individual current activities.
    """
    map={
        "Artificial intelligence / machine learning": "AI/ML",
        "Bioinformatics": "Bioinformatics",
        "Data collection, analysis, and visualization": "Data coll/analysis/vis",
        "Software development and/or maintenance": "Software dev/maintenance"
    }
    df[column] = df[column].str.replace(map)
    return df



def plot_q3_by_division(
    df: pd.DataFrame,
    division_col: str = 'Q1',
    question_col: str = 'Q3',
) -> None:
    """
    Plot individual Q3 responses, broken out by division.

    Q3 is a multi-response question with selections separated by commas.
    Each individual selection is counted separately.

    Parameters
    ----------
    df : pd.DataFrame
        Survey data.
    division_col : str, optional
        Column containing division, by default 'Q1'.
    question_col : str, optional
        Column containing Q3 responses, by default 'Q3'.

    Returns
    -------
    None
    """

    # Keep responses with both Q3 and division reported
    df_plot = df[[question_col, division_col]].dropna().copy()

    # Split multi-select responses and explode into individual rows
    df_plot[question_col] = df_plot[question_col].str.split(',')

    df_plot = df_plot.explode(question_col)

    # Remove whitespace around individual responses
    df_plot[question_col] = df_plot[question_col].str.strip()

    # Remove empty responses, if present
    df_plot = df_plot.loc[df_plot[question_col] != '']

    # Count each individual response by division
    counts = (
        df_plot
        .groupby([question_col, division_col])
        .size()
        .unstack(fill_value=0)
    )

    # Sort Q3 responses by total number of selections
    counts = counts.loc[
        counts.sum(axis=1).sort_values(ascending=True).index
    ]

    # Colorblind-safe palette
    palette = sns.color_palette(
        'colorblind',
        n_colors=len(counts.columns),
    )

    # Plot
    fig, ax = plt.subplots(figsize=(7, 4))

    counts.plot(
        kind='barh',
        stacked=True,
        ax=ax,
        color=palette,
        width=0.9,
    )

    # Formatting
    ax.set_xlabel('Number of Respondents')
    ax.set_ylabel('Current Activities (multiple allowed)')
    # ax.set_title('Q3 Responses by Division')

    ax.legend(
        title='Division',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        frameon=False,
    )

    sns.despine()

    fig.tight_layout()
    plt.show()


def format_q4(df: pd.DataFrame, question_col: str = 'Q4') -> pd.DataFrame:
    """
    Format the Q4 responses in the survey DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the survey data.
    question_col : str, optional
        Column containing Q4 responses, by default 'Q4'.

    Returns
    -------
    pandas.DataFrame
        DataFrame with formatted Q4 responses.
    """
    map = {
        'Research Information Services (RIS)': 'RIS',
        'EPIC or COGITO or Lab IS': 'EPIC/COGITO/Lab IS',
        "LGM Informatics ('CP Informatics')":'CP Informatics',
        'Informatics, Data Science & Biostatistics (I2DB)': 'I2DB',
        'WashU Informatics Core Services':'WU Informatics Core',
        'Center for Translational Bioinformatics (CTBI)': 'CTBI',
        'Center for Biostatistics and Data Science (CBDS)': 'CBDS',
        'Local divisional services': 'Divisional services'
    }
    df[question_col] = df[question_col].str.replace(map)
    return df


def plot_q4_by_division(
    df: pd.DataFrame,
    division_col: str = 'Q1',
    question_col: str = 'Q4',
) -> None:
    """
    Plot individual Q4 responses, broken out by division.

    Q4 is a multi-response question with selections separated by commas.
    Each individual selection is counted separately.

    Parameters
    ----------
    df : pd.DataFrame
        Survey data.
    division_col : str, optional
        Column containing division, by default 'Q1'.
    question_col : str, optional
        Column containing Q4 responses, by default 'Q4'.

    Returns
    -------
    None
    """

    # Keep responses with both Q4 and division reported
    df_plot = df[[question_col, division_col]].dropna().copy()

    # Split multi-select responses and explode into individual rows
    df_plot[question_col] = df_plot[question_col].str.split(',')

    df_plot = df_plot.explode(question_col)

    # Remove whitespace around individual responses
    df_plot[question_col] = df_plot[question_col].str.strip()

    # Remove empty responses, if present
    df_plot = df_plot.loc[df_plot[question_col] != '']

    # Count each individual response by division
    counts = (
        df_plot
        .groupby([question_col, division_col])
        .size()
        .unstack(fill_value=0)
    )

    # Sort Q4 responses by total number of selections
    counts = counts.loc[
        counts.sum(axis=1).sort_values(ascending=True).index
    ]

    # Colorblind-safe palette
    palette = sns.color_palette(
        'colorblind',
        n_colors=len(counts.columns),
    )

    # Plot
    fig, ax = plt.subplots(figsize=(7, 5))

    counts.plot(
        kind='barh',
        stacked=True,
        ax=ax,
        color=palette,
        width=0.9,
    )

    # Formatting
    ax.set_xlabel('Number of Respondents')
    ax.set_ylabel('Resources Used (multiple allowed)')

    ax.legend(
        title='Division',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        frameon=False,
    )

    sns.despine()

    fig.tight_layout()
    plt.show()

def format_q5(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format Q5 responses by stripping whitespace and handling missing values.

    Parameters
    ----------
    df : pd.DataFrame
        Survey data.

    Returns
    -------
    pd.DataFrame
        DataFrame with formatted Q5 responses.
    """
    map = {
        'Limited knowledge or familiarity':'Limited knowledge',
        'Clinical application support is insufficient':'Insuff clin app supp',
        'Lack of computational resources (compute or storage)':'Lack of compute or storage',
        'Difficulty obtaining clinical data or specimens':'Diff obtaining clin data or spec',
        'Lack of data analysis or visualization support':'Lack of data analysis or viz supp',
        'I have not experienced significant limitations':'No significant limitations',
    }
    df['Q5'] = df['Q5'].str.replace(map)
    return df


def plot_q5_by_division(
    df: pd.DataFrame,
    division_col: str = 'Q1',
    question_col: str = 'Q5',
) -> None:
    """
    Plot individual Q5 responses, broken out by division.

    Q5 is a multi-response question with selections separated by commas.
    Each individual selection is counted separately.

    Parameters
    ----------
    df : pd.DataFrame
        Survey data.
    division_col : str, optional
        Column containing division, by default 'Q1'.
    question_col : str, optional
        Column containing Q5 responses, by default 'Q5'.

    Returns
    -------
    None
    """

    # Keep responses with both Q5 and division reported
    df_plot = df[[question_col, division_col]].dropna().copy()

    # Split multi-select responses
    df_plot[question_col] = df_plot[question_col].str.split(',')

    # Explode so each selection gets its own row
    df_plot = df_plot.explode(question_col)

    # Clean whitespace
    df_plot[question_col] = df_plot[question_col].str.strip()

    # Remove empty responses
    df_plot = df_plot.loc[df_plot[question_col] != '']

    # Count each response by division
    counts = (
        df_plot
        .groupby([question_col, division_col])
        .size()
        .unstack(fill_value=0)
    )

    # Sort responses by total number of selections
    counts = counts.loc[
        counts.sum(axis=1).sort_values(ascending=True).index
    ]

    # Colorblind-safe palette
    palette = sns.color_palette(
        'colorblind',
        n_colors=len(counts.columns),
    )

    # Plot
    fig, ax = plt.subplots(figsize=(7, 5))

    counts.plot(
        kind='barh',
        stacked=True,
        ax=ax,
        color=palette,
        width=0.9,
    )

    # Formatting
    ax.set_xlabel('Number of Respondents')
    ax.set_ylabel('Q5 Responses (multiple allowed)')

    ax.legend(
        title='Division',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        frameon=False,
    )

    sns.despine()

    fig.tight_layout()
    plt.show()


def plot_q7_likert_diverging(
    df: pd.DataFrame,
) -> None:
    """
    Plot Q7 as a diverging Likert chart.

    The neutral/middle response ('Moderately') is centered on zero.
    Half of the moderate responses extend to the left and half to the right.

    Responses are normalized to percentages within each question.
    """

    question_map = {
        'Q7_1': 'AI governance, guidance, and policy',
        'Q7_2': 'AI education and consultation',
        'Q7_3': 'Bioinformatics',
        'Q7_4': 'Clinical application support',
        'Q7_5': 'Clinical data access',
        'Q7_6': 'Data analytics and visualization',
        'Q7_7': 'Educational workshops',
        'Q7_8': 'Shared computing infrastructure',
        'Q7_9': 'Single point of entry for informatics and data science needs',
        'Q7_10': 'Software/application development support',
    }

    likert_map = {
        'Not valuable': 1,
        'Slightly': 2,
        'Moderately': 3,
        'Very': 4,
        'Essential': 5,
    }

    likert_labels = {
        1: 'Not valuable',
        2: 'Slightly',
        3: 'Moderately',
        4: 'Very',
        5: 'Essential',
    }

    question_cols = list(question_map.keys())

    # -------------------------------------------------------------------------
    # Reshape data
    # -------------------------------------------------------------------------

    df_long = (
        df[question_cols]
        .rename(columns=question_map)
        .melt(
            var_name='Resource',
            value_name='Response',
        )
        .dropna(subset=['Response'])
    )

    df_long['Response'] = (
        df_long['Response']
        .astype(str)
        .str.strip()
    )

    df_long['Rating'] = df_long['Response'].map(likert_map)

    df_long = df_long.dropna(subset=['Rating'])

    df_long['Rating'] = df_long['Rating'].astype(int)

    # -------------------------------------------------------------------------
    # Calculate response percentages
    # -------------------------------------------------------------------------

    counts = (
        df_long
        .groupby(
            ['Resource', 'Rating'],
            observed=True,
        )
        .size()
        .unstack(fill_value=0)
        .reindex(columns=[1, 2, 3, 4, 5], fill_value=0)
    )

    percentages = (
        counts
        .div(counts.sum(axis=1), axis=0)
        * 100
    )

    # -------------------------------------------------------------------------
    # Calculate mean rating and sort
    # -------------------------------------------------------------------------

    means = (
        df_long
        .groupby('Resource')['Rating']
        .mean()
        .sort_values()
    )

    percentages = percentages.loc[means.index]
    means = means.loc[percentages.index]

    # -------------------------------------------------------------------------
    # Diverging coordinates
    #
    # Moderate is split evenly around zero:
    #
    #  <------------ | ------------>
    #   1    2    3  |  3    4    5
    #
    # -------------------------------------------------------------------------

    p1 = percentages[1]
    p2 = percentages[2]
    p3 = percentages[3]
    p4 = percentages[4]
    p5 = percentages[5]

    half_neutral = p3 / 2

    # Blue -> neutral -> red
    colors = sns.color_palette(
        'RdBu_r',
        n_colors=5,
    )

    # -------------------------------------------------------------------------
    # Plot
    # -------------------------------------------------------------------------

    fig, ax = plt.subplots(figsize=(10, 6))

    y = range(len(percentages))

    # -------------------------
    # Negative side
    # -------------------------

    # Moderately: left half
    ax.barh(
        y,
        -half_neutral,
        left=0,
        color=colors[2],
        height=0.8,
    )

    # Slightly
    ax.barh(
        y,
        -p2,
        left=-half_neutral,
        color=colors[1],
        height=0.8,
    )

    # Not valuable
    ax.barh(
        y,
        -p1,
        left=-(half_neutral + p2),
        color=colors[0],
        height=0.8,
    )

    # -------------------------
    # Positive side
    # -------------------------

    # Moderately: right half
    ax.barh(
        y,
        half_neutral,
        left=0,
        color=colors[2],
        height=0.8,
    )

    # Very
    ax.barh(
        y,
        p4,
        left=half_neutral,
        color=colors[3],
        height=0.8,
    )

    # Essential
    ax.barh(
        y,
        p5,
        left=half_neutral + p4,
        color=colors[4],
        height=0.8,
    )

    # -------------------------------------------------------------------------
    # Formatting
    # -------------------------------------------------------------------------

    ax.set_yticks(list(y))
    ax.set_yticklabels(percentages.index)

    ax.set_xlabel('Respondents (%)')
    ax.set_ylabel('')

    # Center line = midpoint of Moderate
    ax.axvline(
        0,
        color='0.3',
        linewidth=0.8,
    )

    # Make left/right range symmetric
    max_extent = max(
        (half_neutral + p2 + p1).max(),
        (half_neutral + p4 + p5).max(),
    )

    # Round upward for cleaner axis limits
    max_extent = min(
        100,
        ((max_extent // 10) + 1) * 10,
    )

    ax.set_xlim(-max_extent, max_extent)

    # Show absolute values on x-axis
    ticks = ax.get_xticks()

    ax.set_xticks(ticks)
    ax.set_xticklabels(
        [f'{abs(x):.0f}' for x in ticks]
    )

    # -------------------------------------------------------------------------
    # Legend
    # -------------------------------------------------------------------------

    from matplotlib.patches import Patch

    legend_handles = [
        Patch(
            facecolor=colors[i],
            label=likert_labels[i + 1],
        )
        for i in range(5)
    ]

    ax.legend(
        handles=legend_handles,
        title='Value',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        frameon=False,
    )

    sns.despine(
        ax=ax,
        left=False,
    )

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
    format_curr_activities(df)
    plot_q3_by_division(df)
    format_q4(df)
    plot_q4_by_division(df)
    format_q5(df)
    plot_q5_by_division(df)
    plot_q7_likert_diverging(df)
    return df

if __name__ == "__main__":
    df = main()



# %%
