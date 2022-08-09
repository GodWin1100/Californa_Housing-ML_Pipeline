import os
from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.exception import HousingException
from housing.logger import logging
import tarfile
from urllib import request  # for high level http requests it's recommended to use requests package
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

# downloading files in python
# https://www.codingem.com/python-download-file-from-url/
# from six.moves import urllib  # six.moves contains packages which has backward compatibility for python2 and python3


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousingException(e) from e

    def download_housing_data(self) -> str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            if os.path.exists(tgz_download_dir):
                # won't be triggered as it's timestamp based
                os.remove(tgz_download_dir)
            os.makedirs(tgz_download_dir, exist_ok=True)
            housing_file_name = os.path.basename(download_url)
            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)
            logging.info(f"Downloading file from {download_url} at {tgz_file_path}")
            request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"{tgz_file_path} Downloaded successfully")
            return tgz_file_path
        except Exception as e:
            raise HousingException(e) from e

    def extract_tgz_file(self, tgz_file_path: str) -> None:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                # won't be triggered as it's timestamp based
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir, exist_ok=True)
            logging.info(f"Extracting {tgz_file_path} into {raw_data_dir}")
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info(f"Extraction completed")
        except Exception as e:
            raise HousingException(e) from e

    def split_data(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            housing_file_path = os.path.join(raw_data_dir, file_name)
            logging.info(f"Reading csv file: {housing_file_path}")
            df_housing = pd.read_csv(housing_file_path)
            df_housing["income_category"] = pd.cut(
                df_housing["median_income"], bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf], labels=[1, 2, 3, 4, 5]
            )
            logging.info(f"Splitting Data into train and test set")
            strat_train_set = None
            strat_test_set = None
            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
            for train_index, test_index in split.split(df_housing, df_housing["income_category"]):
                strat_train_set = df_housing.loc[train_index].drop(["income_category"], axis=1)
                strat_test_set = df_housing.loc[test_index].drop(["income_category"], axis=1)
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting training dataset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index=False)
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=train_file_path,
                test_file_path=test_file_path,
                is_ingested=True,
                message=f"Data Ingestion completed successfully",
            )
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise HousingException(e) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"Data Ingestion Log Started".center(100, "-"))
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data()
        except Exception as e:
            raise HousingException(e) from e

    def __del__(self):
        logging.info(f"Data Ingestion Log Completed".center(100, "-"))
