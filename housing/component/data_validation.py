import json
import os
import pandas as pd
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab


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
            logging.info("Data Validation started")
            validation_status = False
            # TODO: Validating schema of train and test data for
            # No. of Columns
            # Column Name
            # Categorical Column values
            validation_status = True
            if not validation_status:
                message = f"Dataset is not validated"
                raise Exception(message)
            logging.info("Data Validation Successful")
            return validation_status
        except Exception as e:
            raise HousingException(e) from e

    def get_train_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise HousingException(e) from e

    def get_and_save_data_drift_report(self):
        try:
            logging.info(f"Creating Data Drift Report")
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df, test_df = self.get_train_test_df()
            profile.calculate(train_df, test_df)
            # # in actuality we will check for train and test data also but majorly for existed train data and new train data
            report = json.loads(profile.json())
            with open(self.data_validation_config.report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=4)
            logging.info(f"Successfully created Data Drift Report at {self.data_validation_config.report_file_path}")
            return report
        except Exception as e:
            raise HousingException(e) from e

    def save_data_drift_report_page(self):
        try:
            logging.info(f"Creating Data Drift Report Page")
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_test_df()
            dashboard.calculate(train_df, test_df)
            dashboard.save(self.data_validation_config.report_page_file_path)
            logging.info(
                f"Successfully Saved Data Drift Report Page at {self.data_validation_config.report_page_file_path}"
            )
        except Exception as e:
            raise HousingException(e) from e

    def is_data_drift_found(self) -> bool:
        # ! Not functional atm
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return False
        except Exception as e:
            raise HousingException(e) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info(f"Data Validation Log Started".center(100, "-"))
            self.is_train_test_file_exist()
            is_validated = self.validate_dataset_schema()
            self.is_data_drift_found()
            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=is_validated,
                message="Data Validation Performed Successfully",
            )
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e) from e

    def __del__(self):
        logging.info(f"Data Validation Log Completed".center(100, "-"))
