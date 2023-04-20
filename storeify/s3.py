from .base import Store, CDNStore
import io
try:
    import boto3
    from botocore.client import BaseClient
except ImportError:
    boto3 = None


class S3Store(Store):
    bucket: str
    region: str
    acl: str = "private"
    def __init__(
        self,
        key_id: "str|None" = None,
        access_key: "str|None" = None,
        secret_key: "str|None" = None,
        region: str = "us-east-1",
    ) -> None:
        if boto3 == None:
            raise ImportError(
                "Please install with s3 support, pip install storeify[s3]"
            )

        self.client = boto3.client(
            aws_access_key_id=key_id,
            aws_secret_access_key=access_key,
            region_name=region,
        )
        if not credentials_work(self.client):
            raise ValueError("Invalid credentials")

        create_bucket(self.client, "storeify", region, boto3.resource("s3"))


    def put(self, filename: str, data: bytes):
        if type(data) != bytes:
            raise TypeError("Data wasn't bytes")

        try:
            self.client.upload_fileobj(
                io.BytesIO(data),
                self.bucket,
                filename,
                ExtraArgs={"ACL": self.acl}
            )
        except Exception as e:
            raise FileExistsError("The file already exists")


    def get(self, filename:str) -> bytes:
        buf = io.BytesIO()
        try:
            self.client.download_fileobj(
                self.bucket,
                filename,
                buf
            )
        except Exception:
            raise FileNotFoundError("Key doesn't exist")
        else:
            return buf.getvalue()


    def delete(self, filename: str):
        try:
            self.client.delete_object(
                Bucket=self.bucket,
                Key=filename,
            )
        except Exception:
            pass


class S3StoreCDN(S3Store, CDNStore):
    """Public S3 Store as a CDN
    """
    def url(self, filename: str) -> str:
        TEMPLATE = "https://{bucket}.s3.{region}.amazonaws.com/{filename}"
        return TEMPLATE.format(
            bucket=self.bucket,
            region=self.region,
            filename=filename,
        )


def credentials_work(client) -> bool:
    try:
        client.list_buckets()
    except Exception:
        return False
    else:
        return True


def create_bucket(client, name: str, region: str, s3):
    s3.create_bucket(
        Bucket=name,
        ACL='public-read',
        CreateBucketConfiguration={
            "LocationConstraint": region
        },
    )
