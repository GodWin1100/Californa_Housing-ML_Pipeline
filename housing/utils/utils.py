import yaml
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
