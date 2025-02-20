import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')
# ----------------------------------------------------

list_of_files = [
    # ".github/workflows/.gitkeep",
    # ".github/workflows/ci.yml",
    # ".github/workflows/cd.yml",

    # "data/raw/",
    # "data/processed/",
    # "data/features/",

    "data_sources/apis/anomaly_dataset_api/main.py",
    "data_sources/apis/anomaly_dataset_api/requirements.txt",
    "data_sources/apis/anomaly_dataset_api/Dockerfile",

    "pipelines/data_pipeline/kafka_producer/main.py",
    "pipelines/data_pipeline/kafka_producer/requirements.txt",
    "pipelines/data_pipeline/kafka_producer/Dockerfile",
    
    # "pipelines/ml_pipeline",
    "compose.yaml",
]


# ----------------------------------------------------
# Script to create the files and directories 

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")