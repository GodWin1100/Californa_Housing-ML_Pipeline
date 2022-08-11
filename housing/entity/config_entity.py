from collections import namedtuple

#  download_url, download_folder, extracted_folder, file_path, train_dataset_folder, test_dataset_folder
DataIngestionConfig = namedtuple(
    "DataIngestionConfig",
    ["dataset_download_url", "tgz_download_dir", "raw_data_dir", "ingested_train_dir", "ingested_test_dir"],
)

# schema_file_path
DataValidationConfig = namedtuple(
    "DataValidationConfig",
    ["schema_file_path", "report_file_path", "report_page_file_path"],
)

# data_specific_configurations*, transformed_data_dir, preprocessed_object_export_path
DataTransformationConfig = namedtuple(
    "DataTransformationConfig",
    ["add_bedroom_per_room", "transformed_train_dir", "transformed_test_dir", "preprocess_object_file_path"],
)

# model_object_export_path, base_accuracy #! if trained model accuracy less than base_accuracy then reject the model
ModelTrainerConfig = namedtuple(
    "ModelTrainerConfig", ["trained_model_file_path", "base_accuracy", "model_config_file_path"]
)

# file_path of all the existing model in production, timestamp
ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["model_evaluation_file_path", "time_stamp"])

# path to save model
ModelPusherConfig = namedtuple("ModelPusherConfig", ["export_dir_path"])

# configuration of asset required during training
TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])
