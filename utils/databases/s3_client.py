
from typing import Any, Dict, List, Optional
import boto3
from botocore.client import Config

class S3Client:
    """Generic S3 client wrapper for common bucket and object operations."""

    def __init__(self, region: str = "us-east-1", endpoint_url: Optional[str] = None) -> None:
        self.s3 = boto3.client("s3", region_name=region, endpoint_url=endpoint_url, config=Config(s3={"addressing_style":"path"}))

    def create_bucket(self, name: str) -> Dict[str, Any]:
        """Create a bucket by name."""
        return self.s3.create_bucket(Bucket=name)

    def list_objects(self, bucket: str, prefix: str = "") -> List[str]:
        """List object keys in a bucket with optional prefix."""
        resp = self.s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [c["Key"] for c in resp.get("Contents", [])]

    def upload_file(self, bucket: str, key: str, local_path: str) -> None:
        """Upload a local file to a bucket/key."""
        self.s3.upload_file(local_path, bucket, key)

    def download_file(self, bucket: str, key: str, local_path: str) -> None:
        """Download an S3 object to a local path."""
        self.s3.download_file(bucket, key, local_path)

    def delete_object(self, bucket: str, key: str) -> None:
        """Delete an object by key."""
        self.s3.delete_object(Bucket=bucket, Key=key)

    def presigned_url(self, bucket: str, key: str, expires: int = 3600) -> str:
        """Generate a presigned URL for downloading."""
        return self.s3.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires)

def main() -> None:
    print("S3Client ready. Requires AWS credentials to run real operations.")

if __name__ == "__main__":
    main()
