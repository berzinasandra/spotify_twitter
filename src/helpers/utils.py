import pandas as pd
from pandas import DataFrame
from typing import Any
import logging
from glob import glob


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Utils")
logger.setLevel(logging.INFO)

def save_as_parquet(df: DataFrame, output_path:str) -> None:
    """Save given Dataframe locally to output path

    Args:
        df (DataFrame): DataFrame to save
        output_path (str): path where to save parquet file

    Returns:
        None, writes to disk
    """
    logger.info(f"Saving DataFrame locally to {output_path} as parquet file.")
    df.to_parquet(output_path)

def read_file(file:str) -> DataFrame:
    """Reads parquet files as DataFrame

    Args:
        file (str): file to read

    Returns:
        DataFrame: file context in DataFrame
    """
    logger.info(f"reading file {file}") 
    return pd.read_parquet(file)

def list_files(path:str) -> list[str]:
    """Lists files in given path 

    Args:
        path (str): local path

    Returns:
        list[str]: list of files in given path
    """
    files = [f for f in glob(f"{path}/*.parquet")]
    logger.info(f"Found raw {len(files)} files in path {path} - {files}")
    return files

