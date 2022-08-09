from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import os


class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HousingException(e) from e

    def is_train_test_file_exist(self) -> bool:
        try:
            is_train_file_exist = False
            is_test_file_exist = False
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)
            is_available = is_train_file_exist and is_test_file_exist
            logging.info(f"Is train and test file exists? {is_available}")
            if not is_available:
                message = f"Training File: {train_file_path} or Testing File: {test_file_path} is not present"
                raise Exception(message)
            return is_available
        except Exception as e:
            raise HousingException(e) from e

    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False
            validation_status = True
            return validation_status
        except Exception as e:
            raise HousingException(e) from e

    def initiate_data_validation(self):
        try:
            logging.info(f"Data Validation Log Started".center(100, "-"))
            self.is_train_test_file_exist()
        except Exception as e:
            raise HousingException(e) from e

    def __del__(self):
        logging.info(f"Data Validation Log Completed".center(100, "-"))
