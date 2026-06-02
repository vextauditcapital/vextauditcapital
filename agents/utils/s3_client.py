import os
import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

logger = logging.getLogger("vext-s3-client")

class S3AssetManager:
    """
    Enterprise Asset Manager supporting AWS S3, DigitalOcean Spaces, and Google Cloud Storage.
    Automatically uploads compiled PDF reports and invoices to private cloud storage
    and generates secure, cryptographically signed, temporary expiring pre-signed URLs.
    
    Includes a seamless fallback to local disk storage in case cloud credentials are not supplied.
    """
    def __init__(self):
        # Read parameters from environment / .env
        self.bucket_name = os.getenv("S3_BUCKET_NAME", "vextaudit-assets")
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region_name = os.getenv("AWS_REGION_NAME", "ap-south-1") # Mumbai/India region default
        
        # Supporting custom endpoints for S3-compatible providers (DigitalOcean Spaces, Supabase Storage, etc.)
        self.endpoint_url = os.getenv("S3_ENDPOINT_URL") 
        
        self.s3_client = None
        self.is_active = False
        
        if self.aws_access_key and self.aws_secret_key:
            try:
                session = boto3.Session(
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key,
                    region_name=self.region_name
                )
                
                client_kwargs = {}
                if self.endpoint_url:
                    client_kwargs["endpoint_url"] = self.endpoint_url
                    
                self.s3_client = session.client('s3', **client_kwargs)
                self.is_active = True
                logger.info("Successfully connected to S3/Cloud Storage Asset Service.")
            except Exception as e:
                logger.warning(f"S3 client initialisation failed: {e}. Falling back to local storage.")
        else:
            logger.info("S3 credentials not found in environment. Asset manager running in Local Fallback Mode.")

    def upload_file(self, local_file_path: str, s3_object_name: str = None) -> str:
        """
        Uploads a local file (e.g. invoices/VAC-1042.pdf) to Cloud Storage.
        Returns the public/pre-signed URL, or local relative path if in fallback mode.
        """
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"Local file not found at {local_file_path}")
            
        if s3_object_name is None:
            s3_object_name = os.path.basename(local_file_path)
            
        # Ensure we use slashes for S3 key
        s3_object_name = s3_object_name.replace('\\', '/')
        
        if self.is_active:
            try:
                # Upload with Content-Type header to ensure browsers render PDF correctly instead of downloading
                extra_args = {"ContentType": "application/pdf"}
                self.s3_client.upload_file(
                    local_file_path,
                    self.bucket_name,
                    s3_object_name,
                    ExtraArgs=extra_args
                )
                logger.info(f"Successfully uploaded {local_file_path} to S3 bucket {self.bucket_name}/{s3_object_name}")
                
                # Generate a temporary pre-signed URL valid for 7 days (604800 seconds)
                return self.generate_presigned_url(s3_object_name, expiration=604800)
            except NoCredentialsError:
                logger.warning("AWS/S3 credentials not available. Saving asset locally.")
            except ClientError as e:
                logger.error(f"S3 upload error: {e}. Saving asset locally.")
                
        # Fallback mode: return local absolute/relative path
        return f"file:///{os.path.abspath(local_file_path)}"

    def generate_presigned_url(self, s3_object_name: str, expiration: int = 604800) -> str:
        """
        Generates a secure, temporary pre-signed GET URL for a private S3 asset.
        """
        if not self.is_active:
            # Fallback path
            return f"file:///opt/vext-audit/{s3_object_name}"
            
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_object_name
                },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logger.error(f"Failed to generate pre-signed URL for {s3_object_name}: {e}")
            return f"file:///opt/vext-audit/{s3_object_name}"

# Global singleton
cloud_assets = S3AssetManager()
