import boto3
import os

def download_zip_from_s3(bucket_name, object_key, download_path="./research/ct_kidney_data.zip"):
    """
    Downloads a ZIP file from S3 and saves it locally (no extraction).
    """
    print(f"Connecting to S3: bucket = {bucket_name}, key = {object_key}")
    s3 = boto3.client('s3')

    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    
    with open(download_path, 'wb') as f:
        print(f"Downloading to {download_path} ...")
        s3.download_fileobj(bucket_name, object_key, f)

    print("Download complete. File saved at:", download_path)

if __name__ == "__main__":
    BUCKET_NAME = "ct-kidney-data"             
    OBJECT_KEY = "ct-kidney-images-data.zip"          
    LOCAL_PATH = "./research/ct_kidney_data.zip"

    download_zip_from_s3(BUCKET_NAME, OBJECT_KEY, LOCAL_PATH)
