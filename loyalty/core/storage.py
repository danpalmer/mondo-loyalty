from django_s3_storage.storage import S3Storage


class PublicS3Storage(S3Storage):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("aws_s3_bucket_auth", False)
        super(PublicS3Storage, self).__init__(*args, **kwargs)
