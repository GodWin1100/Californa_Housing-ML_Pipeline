from collections import namedtuple

# data file paths, boolean for status, message
DataIngestionArtifact = namedtuple(
    "DataIngestionArtifact", ["train_file_path", "test_file_path", "is_ingested", "message"]
)

# data schema file path, report file path, report page path, boolean for status, message
DataValidationArtifact = namedtuple(
    "DataValidationArtifact",
    ["schema_file_path", "report_file_path", "report_page_file_path", "is_validated", "message"],
)

# boolean for status, message, transformed data path, preprocessed object path (transformer serialized object)
DataTransformationArtifact = namedtuple(
    "DataTransformationArtifact",
    [
        "is_transformed",
        "message",
        "transformed_train_file_path",
        "transformed_test_file_path",
        "preprocessed_object_file_path",
    ],
)

# boolean for status, message, trained model file path, metric for train and test data, model accuracy
ModelTrainerArtifact = namedtuple(
    "ModelTrainerArtifact",
    [
        "is_trained",
        "message",
        "trained_model_file_path",
        "train_rmse",
        "test_rmse",
        "train_accuracy",
        "test_accuracy",
        "model_accuracy",
    ],
)

# boolean for status, path of evaluated model
ModelEvaluationArtifact = namedtuple("ModelEvaluationArtifact", ["is_model_accepted", "evaluated_model_path"])

# boolean for status, path of exported model
ModelPusherArtifact = namedtuple("ModelPusherArtifact", ["is_model_pusher", "export_model_file_path"])
