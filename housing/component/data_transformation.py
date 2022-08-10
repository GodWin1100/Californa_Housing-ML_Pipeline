import os
import numpy as np
import pandas as pd
from housing.config.configuration import Configuration
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from housing.entity.config_entity import DataTransformationConfig
from housing.exception import HousingException
from housing.logger import logging
from housing.constants import *
from housing.utils.utils import read_yaml_file, save_object, save_numpy_array_data, load_data
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


class FeatureGenerator(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        add_bedrooms_per_room: bool = True,
        total_rooms_idx: int = 3,
        population_idx: int = 5,
        households_idx: int = 6,
        total_bedrooms_idx: int = 4,
        columns: list = None,
    ):
        """Generate Additional Feature for prediction

        Args:
            add_bedrooms_per_room (bool, optional): To add bedrooms_per_room feature. Defaults to True.
            total_rooms_idx (int, optional): index of total_rooms. Defaults to 3.
            population_idx (int, optional): index of population. Defaults to 5.
            households_idx (int, optional): index of households. Defaults to 6.
            total_bedrooms_idx (int, optional): index of total_bedrooms. Defaults to 4.
            columns (list, optional): list of columns of dataframe in same sequence to get index of feature. Defaults to None.
        """
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_idx = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_idx = self.columns.index(COLUMN_POPULATION)
                households_idx = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_idx = self.columns.index(COLUMN_TOTAL_BEDROOMS)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_idx = total_rooms_idx
            self.population_idx = population_idx
            self.households_idx = households_idx
            self.total_bedrooms_idx = total_bedrooms_idx
        except Exception as e:
            raise HousingException(e) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X: np.ndarray, y: np.ndarray = None) -> np.ndarray:
        """Add additional feature at last position of columns in the following sequence:
            Data, room_per_household, population_per_household, bedrooms_per_room

        Args:
            X (np.ndarray): Feature Data
            y (np.ndarray, optional): Target. Defaults to None.

        Raises:
            HousingException: Exception

        Returns:
            np.ndarray: return data with additional feature
        """
        try:
            room_per_household = X[:, self.total_rooms_idx] / X[:, self.households_idx]
            population_per_household = X[:, self.population_idx] / X[:, self.households_idx]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_idx] / X[:, self.total_rooms_idx]
                generated_feature = np.c_[X, room_per_household, population_per_household, bedrooms_per_room]
            else:
                # or np.hstack
                generated_feature = np.c_[X, room_per_household, population_per_household]
            return generated_feature
        except Exception as e:
            raise HousingException(e) from e


class DataTransformation:
    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact,
    ):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise HousingException(e) from e

    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml_file(schema_file_path)
            numerical_columns = dataset_schema[SCHEMA_NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[SCHEMA_CATEGORICAL_COLUMN_KEY]
            num_pipe = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    (
                        "feature_gen",
                        FeatureGenerator(
                            add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                            columns=numerical_columns,
                        ),
                    ),
                    ("scaler", StandardScaler()),
                ]
            )
            cat_pipe = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("ohe", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )  # with_mean=False is due to sparse matrix from OneHotEncoder
            logging.info(f"Numerical Column: {numerical_columns}")
            logging.info(f"Categorical Column: {categorical_columns}")
            preprocessing = ColumnTransformer(
                [("num_pipeline", num_pipe, numerical_columns), ("cat_pipeline", cat_pipe, categorical_columns)]
            )
            return preprocessing
        except Exception as e:
            raise HousingException(e) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"Data Transformation Log Started".center(100, "-"))
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            schema_file_path = self.data_validation_artifact.schema_file_path
            schema = read_yaml_file(schema_file_path)
            target_column_name = schema[TARGET_COLUMN_KEY]

            logging.info("Loaded training and testing data")
            # loading training and test data
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            # input and target feature
            input_feature_train_df = train_df.drop([target_column_name], axis=1)
            target_feature_train_df = train_df[[target_column_name]]
            input_feature_test_df = test_df.drop([target_column_name], axis=1)
            target_feature_test_df = test_df[[target_column_name]]

            logging.info("Preprocessing and transforming data")
            # preprocessing data
            preprocessing_obj = self.get_data_transformer_object()
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # concatenating data
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # storing data
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv", ".npz")

            logging.info("Storing transformed data")
            transformed_train_file_path = os.path.join([transformed_train_dir, train_file_name])
            transformed_test_file_path = os.path.join([transformed_test_dir, test_file_name])
            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)
            logging.info(f"Stored Transformed Train Data at {transformed_train_file_path}")
            logging.info(f"Stored Transformed Test Data at {transformed_test_file_path}")

            # storing preprocessing object
            preprocessing_obj_filepath = self.data_transformation_config.preprocess_object_file_path
            save_object(preprocessing_obj_filepath, preprocessing_obj)
            logging.info(f"Stored Preprocessing Object at {preprocessing_obj_filepath}")

            data_transformation_artifact = DataTransformationArtifact(
                is_transformed=True,
                message="Data Transformed Successfully",
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                preprocessed_object_file_path=preprocessing_obj_filepath,
            )
            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise HousingException(e) from e

    def __del__(self):
        logging.info(f"Data Transformation Log Completed".center(100, "-"))
