"""
AWS Configuration
-----------------
Configuration settings for AWS services.
"""


# AWS Region
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# S3 Configuration
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'alignment-tax-results')
S3_RESULTS_PREFIX = 'runs/'
S3_LOGS_PREFIX = 'logs/'

# Secrets Manager Configuration
SECRETS_OPENAI_KEY_NAME = os.getenv('SECRETS_OPENAI_KEY_NAME', 'alignment-tax/openai-api-key')

# EC2 Configuration
EC2_INSTANCE_TYPE = os.getenv('EC2_INSTANCE_TYPE', 't3.xlarge')  # 4 vCPUs, 16GB RAM
EC2_SECURITY_GROUP_NAME = 'alignment-tax-sg'
EC2_KEY_PAIR_NAME = os.getenv('EC2_KEY_PAIR_NAME', None)  # Optional SSH key

# IAM Role Configuration
IAM_ROLE_NAME = 'alignment-tax-ec2-role'
IAM_POLICY_DOCUMENT = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                f"arn:aws:s3:::{S3_BUCKET_NAME}/*",
                f"arn:aws:s3:::{S3_BUCKET_NAME}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": f"arn:aws:secretsmanager:{AWS_REGION}:*:secret:{SECRETS_OPENAI_KEY_NAME}*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}

# Environment Detection
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')  # 'local' or 'aws'

# Paths based on environment
if ENVIRONMENT == 'aws':
    BASE_PATH = '/app'
    RESULTS_PATH = '/app/results'
    LOGS_PATH = '/app/logs'
    MODELS_PATH = '/app/models'
else:
    # Use local paths from Config
    BASE_PATH = None  # Will use paths from 01-Config.py
    RESULTS_PATH = None
    LOGS_PATH = None
    MODELS_PATH = None


def is_aws_environment():
    """Check if running in AWS environment"""
    return ENVIRONMENT == 'aws'


def get_results_path():
    """Get appropriate results path based on environment"""
    if is_aws_environment():
        return RESULTS_PATH
    else:
        # Import from local config
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../src')
        from Config import base_results_path
        return base_results_path


def validate_aws_environment():
    """
    Validate that required environment variables are set when running in AWS mode.
    Prints warnings for missing optional variables.

    Returns:
        True if all required variables are set, False otherwise
    """
    if not is_aws_environment():
        return True  # Not in AWS mode, no validation needed

    print("\n🔍 Validating AWS environment...")

    required_vars = ['AWS_REGION', 'S3_BUCKET_NAME']
    optional_vars = ['SECRETS_OPENAI_KEY_NAME', 'EC2_INSTANCE_TYPE']

    missing_required = []
    missing_optional = []

    # Check required variables
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)

    # Check optional variables
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)

    # Report results
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print(f"   Set these variables before running in AWS mode")
        return False

    if missing_optional:
        print(f"⚠️  Optional variables not set (using defaults): {', '.join(missing_optional)}")

    print(f"✅ AWS environment validated")
    print(f"   Region: {AWS_REGION}")
    print(f"   S3 Bucket: {S3_BUCKET_NAME}")

    return True


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 2025

@author: ramyalsaffar
"""
