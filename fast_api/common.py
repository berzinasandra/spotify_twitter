import pandas as pd
from pandas import DataFrame

from src.helpers.utils import list_files


def read_all_files(path) -> DataFrame:
    """Gathers all details in Spotify Processed directory into one DataFrame

    Returns:
        DataFrame: all song details in DataFrame
    """
    files = list_files(path)
    all_dfs: list = []
    for file in files:
        df = pd.read_parquet(file)
        all_dfs.append(df)
    main_df = pd.concat(all_dfs)
    return main_df
