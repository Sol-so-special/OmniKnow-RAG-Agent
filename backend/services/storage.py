import boto3
from google.cloud import storage as gcs
from pathlib import Path
from core.config import get_settings
import logging
import tempfile

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        self.bucket_name = None
        self.storage_type = "local"  # Default

        if self.settings.environment == "production":
            cloud = self.settings.cloud_provider
            
            if cloud == "gcp":
                if not self.settings.gcs_bucket_name:
                    raise ValueError("GCS_BUCKET_NAME required when CLOUD_PROVIDER=gcp")
                
                # Initialize GCS client (uses default credentials)
                if self.settings.gcs_project_id:
                    self.client = gcs.Client(project=self.settings.gcs_project_id)
                else:
                    self.client = gcs.Client()  # Uses default project
                
                self.bucket_name = self.settings.gcs_bucket_name
                self.bucket = self.client.bucket(self.bucket_name)
                self.storage_type = "gcs"
                logger.info(f"Using GCS bucket: {self.bucket_name}")
                
            elif cloud == "aws":
                if not self.settings.s3_bucket_name:
                    raise ValueError("S3_BUCKET_NAME required when CLOUD_PROVIDER=aws")
                
                self.client = boto3.client('s3', region_name=self.settings.s3_region)
                self.bucket_name = self.settings.s3_bucket_name
                self.storage_type = "s3"
                logger.info(f"Using S3 bucket: {self.bucket_name}")
                
            else:
                logger.warning("Production mode but CLOUD_PROVIDER not set. Using local storage.")
                self.storage_type = "local"
        
        if self.storage_type == "local":
            self.local_dir = Path(self.settings.upload_directory)
            self.local_dir.mkdir(exist_ok=True)
            logger.info(f"Using local storage: {self.local_dir}")
    
    def save_file(self, filename: str, content: bytes) -> str:
        """Save file to storage."""
        key = f"uploads/{filename}"

        if self.storage_type == "s3":
            self.client.put_object(Bucket=self.bucket_name, Key=key, Body=content)
            logger.info(f"Uploaded to S3: {key}")
            return f"s3://{self.bucket_name}/{key}"
        elif self.storage_type == "gcs":
            blob = self.bucket.blob(key)
            blob.upload_from_string(content)
            logger.info(f"Uploaded to GCS: {key}")
            return f"gs://{self.bucket_name}/{key}"
        else:  # local
            # Save locally
            file_path = self.local_dir / filename
            with open(file_path, 'wb') as f:
                f.write(content)
            logger.info(f"Saved locally: {file_path}")
            return str(file_path)
    
    def get_file_path(self, filename: str) -> str:
        """Get file path for processing."""
        key = f"uploads/{filename}"
        temp_path = Path(tempfile.gettempdir()) / filename

        if self.storage_type == "s3":
            self.client.download_file(self.bucket_name, key, str(temp_path))
            logger.info(f"Downloaded from S3 to: {temp_path}")
            return str(temp_path)
        elif self.storage_type == "gcs":
            blob = self.bucket.blob(key)
            blob.download_to_filename(str(temp_path))
            logger.info(f"Downloaded from GCS to: {temp_path}")
            return str(temp_path)
        else:  # local
            return str(self.local_dir / filename)