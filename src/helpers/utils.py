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
        df (DataFrame): _description_
        output_path (str): 
    """
    logger.info(f"Saving DataFrame locally to {output_path} as parquet file.")
    df.to_parquet(output_path)

def read_file(file:str) -> DataFrame:
    """_summary_

    Args:
        file (str): _description_

    Returns:
        DataFrame: _description_
    """
    logger.info(f"reading file {file}") 
    return pd.read_parquet(file)

def list_files(path:str) -> list[str]:
    """_summary_

    Args:
        path (str): _description_

    Returns:
        list[str]: _description_
    """
    files = [f for f in glob(f"{path}/*.parquet")]
    logger.info(f"Found raw {len(files)} files in path {path} - {files}")
    return files

