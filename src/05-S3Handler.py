"""
AWS S3 Handler
--------------
Handles all S3 operations for storing results, logs, and intermediate files.
"""

import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime


class S3Handler:
    """Handle S3 operations for alignment tax project"""

    def __init__(self, bucket_name=None, region='us-east-1'):
        """
        Initialize S3 handler

        Args:
            bucket_name: S3 bucket name (default: alignment-tax-results)
            region: AWS region (default: us-east-1)
        """
        self.bucket_name = bucket_name or 'alignment-tax-results'
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)

        # Ensure bucket exists
        self._ensure_bucket_exists()


    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"✅ S3 bucket '{self.bucket_name}' exists")
        except ClientError:
            print(f"📦 Creating S3 bucket '{self.bucket_name}'...")
            try:
                if self.region == 'us-east-1':
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                else:
                    self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                print(f"✅ Bucket created successfully")
            except ClientError as e:
                print(f"❌ Error creating bucket: {e}")
                raise


    def upload_file(self, local_file_path, s3_key=None, metadata=None):
        """
        Upload file to S3

        Args:
            local_file_path: Path to local file
            s3_key: S3 object key (default: filename with timestamp)
            metadata: Optional metadata dictionary

        Returns:
            S3 key of uploaded file
        """
        if s3_key is None:
            filename = os.path.basename(local_file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            s3_key = f"results/{timestamp}/{filename}"

        try:
            extra_args = {}
            if metadata:
                extra_args['Metadata'] = metadata

            self.s3_client.upload_file(
                local_file_path,
                self.bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )

            print(f"✅ Uploaded {local_file_path} to s3://{self.bucket_name}/{s3_key}")
            return s3_key

        except ClientError as e:
            print(f"❌ Error uploading file: {e}")
            raise


    def upload_results(self, results_dir, run_id):
        """
        Upload all results for a run

        Args:
            results_dir: Directory containing results
            run_id: Run identifier

        Returns:
            List of uploaded S3 keys
        """
        uploaded_keys = []

        print(f"\n📤 Uploading results for run {run_id}...")

        # Upload all files in results directory
        for root, dirs, files in os.walk(results_dir):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, results_dir)
                s3_key = f"runs/{run_id}/{relative_path}"

                try:
                    uploaded_key = self.upload_file(local_path, s3_key)
                    uploaded_keys.append(uploaded_key)
                except Exception as e:
                    print(f"⚠️ Failed to upload {file}: {e}")

        print(f"✅ Uploaded {len(uploaded_keys)} files to S3")
        return uploaded_keys


    def download_file(self, s3_key, local_file_path):
        """
        Download file from S3

        Args:
            s3_key: S3 object key
            local_file_path: Path to save file locally
        """
        try:
            self.s3_client.download_file(
                self.bucket_name,
                s3_key,
                local_file_path
            )
            print(f"✅ Downloaded s3://{self.bucket_name}/{s3_key} to {local_file_path}")
        except ClientError as e:
            print(f"❌ Error downloading file: {e}")
            raise


    def list_runs(self):
        """
        List all runs in S3

        Returns:
            List of run IDs
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='runs/',
                Delimiter='/'
            )

            if 'CommonPrefixes' in response:
                runs = [prefix['Prefix'].split('/')[1] for prefix in response['CommonPrefixes']]
                return sorted(runs, reverse=True)
            else:
                return []

        except ClientError as e:
            print(f"❌ Error listing runs: {e}")
            return []


    def upload_logs(self, log_file_path, run_id):
        """
        Upload log file to S3

        Args:
            log_file_path: Path to log file
            run_id: Run identifier

        Returns:
            S3 key of uploaded log
        """
        s3_key = f"logs/{run_id}/{os.path.basename(log_file_path)}"
        return self.upload_file(log_file_path, s3_key)


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 2025

@author: ramyalsaffar
"""
