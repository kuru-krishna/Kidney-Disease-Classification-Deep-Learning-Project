import os
import zipfile
import gdown
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> str:
        '''
        Fetch data from the url and save it locally
        '''
        try: 
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs(self.config.root_dir, exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            # Correct URL construction
            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?export=download&id='
            full_url = prefix + file_id

            gdown.download(full_url, str(zip_download_dir), quiet=False)

            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            raise e

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        """
        try:
            unzip_path = self.config.unzip_dir
            os.makedirs(unzip_path, exist_ok=True)
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
            logger.info(f"Extracted zip file into: {unzip_path}")
        except Exception as e:
            logger.error(f"Failed to extract zip file: {e}")
            raise e