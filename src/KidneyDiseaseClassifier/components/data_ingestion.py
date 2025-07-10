import os
import zipfile
import boto3
from urllib.parse import urlparse
from KidneyDiseaseClassifier import logger
from KidneyDiseaseClassifier.utils.common import get_size
from KidneyDiseaseClassifier.entity.config_entity import (DataIngestionConfig)



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> str:
        '''
        Downloads ZIP file from an S3 public URL and saves it locally.
        '''
        try:
            dataset_url = self.config.source_URL
            zip_download_path = self.config.local_data_file
            os.makedirs(os.path.dirname(zip_download_path), exist_ok=True)

            logger.info(f"Downloading data from {dataset_url} into {zip_download_path}")

            # Parse bucket and key from the S3 URL
            parsed_url = urlparse(dataset_url)
            bucket_name = parsed_url.netloc.split('.')[0]  
            object_key = parsed_url.path.lstrip('/')       

            s3 = boto3.client('s3')
            with open(zip_download_path, 'wb') as f:
                s3.download_fileobj(bucket_name, object_key, f)

            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_path}")
            return zip_download_path

        except Exception as e:
            logger.error(f"Failed to download file from S3: {e}")
            raise e

    def extract_zip_file(self):
        """
        Extracts the downloaded ZIP file into the target directory.
        """
        try:
            unzip_path = self.config.unzip_dir
            zip_path = self.config.local_data_file

            os.makedirs(unzip_path, exist_ok=True)
            logger.info(f"Extracting {zip_path} to {unzip_path}")

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)

            logger.info(f"Extraction completed to folder: {unzip_path}")

        except Exception as e:
            logger.error(f"Failed to extract zip file: {e}")
            raise e

