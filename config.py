import os

# Load database URL from environment or set default (use environment variables for production)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/pii_db')

# AWS credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'your-access-key')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'your-secret-key')
AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME', 'your-bucket-name')
AWS_REGION = os.environ.get('AWS_REGION', 'your-region')
