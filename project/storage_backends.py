# django
from django.conf import settings

# others libraries
from storages.backends import s3boto3


class S3StaticStorage(s3boto3.S3StaticStorage):
    location = "static"
    default_acl = "public-read"

    def __init__(self, **_settings):
        super().__init__(**_settings)

        if settings.DO_SPACES_CDN_ENABLED:
            # The CDN replies much faster (16ms vs 450ms), but the first GETtakes around
            # 1s.

            # Use the CDN for public files only.

            # For private files which have a non-constant signature, the CDN is actually
            # slower, and the implementation is hacky
            # (def url: return super.url.replace(without_cdn, with_cdn)), as s3boto3
            # doesn't sign when custom_domain is set.

            # If the faster speed of the CDN is preferred for media, delete this `if`
            # block, globally set AWS_S3_CUSTOM_DOMAIN, and in S3MediaStorage below,
            # change default_acl and add "querystring_auth = False".

            self.custom_domain = (
                f"{settings.AWS_STORAGE_BUCKET_NAME}"
                f".{settings.DO_SPACES_REGION}.cdn.digitaloceanspaces.com"
            )


class S3MediaStorage(s3boto3.S3Boto3Storage):
    location = "media"
    default_acl = "private"

    # base.models.file_path method adds a random string.
    # But if it's not used, and an upload tries to overwrite an existing file, for
    # example a.jpg, this setting prevents it by uploading the new one with name
    # a_K7dJ7Ys.jpg
    file_overwrite = False
