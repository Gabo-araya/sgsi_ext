import storages


class S3StaticStorage(storages.backends.s3boto3.S3StaticStorage):
    location = "static"
    default_acl = "public-read"


class S3MediaStorage(storages.backends.s3boto3.S3Boto3Storage):
    location = "media"
    default_acl = "private"
    file_overwrite = False
