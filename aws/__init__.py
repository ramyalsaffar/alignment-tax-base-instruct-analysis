"""
AWS Module
----------
AWS infrastructure handlers for alignment tax experiments.
"""

from .s3_handler import S3Handler
from .secrets_handler import SecretsHandler
from .ec2_setup import EC2Manager
from .config_aws import (
    AWS_REGION,
    S3_BUCKET_NAME,
    SECRETS_OPENAI_KEY_NAME,
    EC2_INSTANCE_TYPE,
    is_aws_environment,
    get_results_path
)

__all__ = [
    'S3Handler',
    'SecretsHandler',
    'EC2Manager',
    'AWS_REGION',
    'S3_BUCKET_NAME',
    'SECRETS_OPENAI_KEY_NAME',
    'EC2_INSTANCE_TYPE',
    'is_aws_environment',
    'get_results_path'
]
