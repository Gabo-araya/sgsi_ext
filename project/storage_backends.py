from storages.backends import s3boto3


class S3StaticStorage(s3boto3.S3StaticStorage):
    location = "static"
    default_acl = "public-read"


class S3MediaStorage(s3boto3.S3Boto3Storage):
    location = "media"
    default_acl = "private"
    file_overwrite = False
