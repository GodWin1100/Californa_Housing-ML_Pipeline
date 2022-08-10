import os
import pickle
import yaml
import numpy as np
import pandas as pd
from housing.constants import *
from housing.exception import HousingException


def read_yaml_file(file_path: str) -> dict:
    """Read yaml file specified at file_path

    Args:
        file_path (str): file path of yaml

    Returns:
        dict: dictionary of yaml configuration
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e) from e


def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HousingException(e) from e


def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousingException(e) from e


def save_object(file_path: str, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise HousingException(e) from e


def load_object(file_path: str):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise HousingException(e) from e


def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(schema_file_path)
        schema = dataset_schema[SCHEMA_COLUMN_KEY]
        dataframe = pd.read_csv(file_path)
        error_message = None
        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message = f"{error_message}\nColumn: [{column}] is not in the schema"
        if error_message:
            raise Exception(error_message)
        return dataframe
    except Exception as e:
        raise HousingException(e) from e
