#
# ? setup.py VS requirements.txt
# https://towardsdatascience.com/requirements-vs-setuptools-python-ae3ee66e28af
# ? setup.py VS requirements.txt with -e .
# https://stackoverflow.com/a/49684835

# # -e . in requirements.txt
# -e, --editable , stands for editable
# -e . , where . stands for the path to setup.py
# -e . will install the mentioned package in editable mode, in this case it will install package at . path i.e. housing package
# if package is installed in editable mode, then any changes made in the package will be reflected without any need to reinstall the package at every changes.


from logging import exception
from setuptools import setup, find_packages

PROJECT_NAME = "California-Housing-Predictor"
VERSION = "0.0.1"
AUTHOR = "GodWin"
DESCRIPTION = "Machine Learning CI/CD Pipeline for California Housing Prediction with Git and Docker."
PACKAGES = [
    "housing"
]  # we can use find_packages to automatically find folder with __init__.py in their root path. For complex setup look into
# https://setuptools.pypa.io/en/latest/userguide/package_discovery.html?highlight=find_packages(#finding-simple-packages
REQUIREMENT_FILE = "./requirements.txt"
EDITABLE = "-e ."


def get_requirements_list() -> list[str]:  # can import from typing package for older python version
    """Return list of packages defined in REQUIREMENT_FILE

    Returns:
        list[str]: list of packages
    """
    try:
        with open(REQUIREMENT_FILE) as requirement_file:
            requirement_list = [requirement.replace("\n", "") for requirement in requirement_file.readlines()]
        if EDITABLE in requirement_list:
            requirement_list.remove(
                EDITABLE
            )  # need to remove -e . as we are using find_packages which is equivalent to -e .
        return requirement_list
    except FileNotFoundError:
        raise Exception("requirements.txt not found at root folder.")


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    # https://setuptools.pypa.io/en/latest/userguide/quickstart.html?highlight=find_packages(#package-discovery
    packages=find_packages(),  # specify the module/folder name which will hold all the packages
    # https://setuptools.pypa.io/en/latest/userguide/quickstart.html?highlight=install_requires#basic-use
    install_requires=get_requirements_list(),  # dependency require with this package
)
