from housing.entity.config_entity import DataIngestionConfig
from housing.exception import HousingException
from housing.logger import logging


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"Data Ingestion Log Started".center(60))
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousingException(e) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise HousingException(e) from e
