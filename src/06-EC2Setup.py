"""
AWS EC2 Setup
-------------
Helper functions for setting up and managing EC2 instances for alignment tax experiments.
"""


class EC2Manager:
    """Manage EC2 instances for alignment tax experiments"""

    def __init__(self, region='us-east-1'):
        """
        Initialize EC2 manager

        Args:
            region: AWS region (default: us-east-1)
        """
        self.region = region
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.ec2_resource = boto3.resource('ec2', region_name=region)


    def get_ubuntu_ami(self):
        """
        Get latest Ubuntu 22.04 LTS AMI

        Returns:
            AMI ID string
        """
        try:
            response = self.ec2_client.describe_images(
                Owners=['099720109477'],  # Canonical (Ubuntu)
                Filters=[
                    {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*']},
                    {'Name': 'state', 'Values': ['available']},
                ],
                MaxResults=1
            )

            if response['Images']:
                ami_id = response['Images'][0]['ImageId']
                print(f"✅ Found Ubuntu 22.04 AMI: {ami_id}")
                return ami_id
            else:
                raise ValueError("No Ubuntu 22.04 AMI found")

        except ClientError as e:
            print(f"❌ Error finding AMI: {e}")
            raise


    def create_security_group(self, group_name='alignment-tax-sg', description='Security group for alignment tax experiments'):
        """
        Create security group with necessary rules

        Args:
            group_name: Security group name
            description: Security group description

        Returns:
            Security group ID
        """
        try:
            # Check if group already exists
            response = self.ec2_client.describe_security_groups(
                Filters=[{'Name': 'group-name', 'Values': [group_name]}]
            )

            if response['SecurityGroups']:
                sg_id = response['SecurityGroups'][0]['GroupId']
                print(f"✅ Security group '{group_name}' already exists: {sg_id}")
                return sg_id

            # Create new security group
            response = self.ec2_client.create_security_group(
                GroupName=group_name,
                Description=description
            )

            sg_id = response['GroupId']
            print(f"✅ Created security group: {sg_id}")

            # Add SSH rule (restrict to your IP in production!)
            self.ec2_client.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'SSH access'}]
                    }
                ]
            )

            print(f"✅ Added SSH ingress rule")
            return sg_id

        except ClientError as e:
            print(f"❌ Error creating security group: {e}")
            raise


    def launch_instance(self, instance_type='t3.xlarge', key_name=None,
                       ami_id=None, security_group_id=None, instance_name='alignment-tax-worker'):
        """
        Launch EC2 instance for running experiments

        Args:
            instance_type: EC2 instance type (default: t3.xlarge - 4 vCPUs, 16GB RAM)
            key_name: SSH key pair name (optional)
            ami_id: AMI ID (default: latest Ubuntu 22.04)
            security_group_id: Security group ID (default: create new)
            instance_name: Name tag for instance

        Returns:
            Instance ID
        """
        print(f"\n🚀 Launching EC2 instance...")
        print(f"   Type: {instance_type}")
        print(f"   Region: {self.region}")

        # Get AMI if not provided
        if ami_id is None:
            ami_id = self.get_ubuntu_ami()

        # Create security group if not provided
        if security_group_id is None:
            security_group_id = self.create_security_group()

        # User data script to set up instance
        user_data_script = """#!/bin/bash
# Update system
apt-get update
apt-get upgrade -y

# Install Python 3.11 and dependencies
apt-get install -y python3.11 python3.11-venv python3-pip git

# Install AWS CLI
apt-get install -y awscli

# Create working directory
mkdir -p /home/ubuntu/alignment-tax
chown ubuntu:ubuntu /home/ubuntu/alignment-tax

# Set up Python virtual environment
cd /home/ubuntu/alignment-tax
python3.11 -m venv venv
source venv/bin/activate

# Install requirements (will be done by Docker or manual setup)
echo "Instance setup complete" > /home/ubuntu/setup_complete.txt
"""

        try:
            # Launch instance
            launch_params = {
                'ImageId': ami_id,
                'InstanceType': instance_type,
                'SecurityGroupIds': [security_group_id],
                'MinCount': 1,
                'MaxCount': 1,
                'UserData': user_data_script,
                'TagSpecifications': [
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {'Key': 'Name', 'Value': instance_name},
                            {'Key': 'Project', 'Value': 'alignment-tax'},
                            {'Key': 'Environment', 'Value': 'production'}
                        ]
                    }
                ],
                'IamInstanceProfile': {'Name': 'alignment-tax-ec2-role'}  # Needs IAM role with S3 and Secrets Manager access
            }

            # Add key pair if provided
            if key_name:
                launch_params['KeyName'] = key_name

            response = self.ec2_client.run_instances(**launch_params)

            instance_id = response['Instances'][0]['InstanceId']
            print(f"✅ Launched instance: {instance_id}")

            # Wait for instance to be running
            print(f"⏳ Waiting for instance to start...")
            waiter = self.ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[instance_id])

            # Get instance details
            instance = self.ec2_resource.Instance(instance_id)
            print(f"✅ Instance running!")
            print(f"   Public IP: {instance.public_ip_address}")
            print(f"   Private IP: {instance.private_ip_address}")

            return instance_id

        except ClientError as e:
            print(f"❌ Error launching instance: {e}")
            raise


    def stop_instance(self, instance_id):
        """Stop EC2 instance"""
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            print(f"✅ Stopping instance {instance_id}")
        except ClientError as e:
            print(f"❌ Error stopping instance: {e}")
            raise


    def terminate_instance(self, instance_id):
        """Terminate EC2 instance"""
        try:
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f"✅ Terminating instance {instance_id}")
        except ClientError as e:
            print(f"❌ Error terminating instance: {e}")
            raise


    def list_instances(self, project_tag='alignment-tax'):
        """
        List all instances for the project

        Args:
            project_tag: Project tag value to filter

        Returns:
            List of instance dictionaries
        """
        try:
            response = self.ec2_client.describe_instances(
                Filters=[
                    {'Name': 'tag:Project', 'Values': [project_tag]},
                    {'Name': 'instance-state-name', 'Values': ['running', 'stopped', 'pending']}
                ]
            )

            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'id': instance['InstanceId'],
                        'type': instance['InstanceType'],
                        'state': instance['State']['Name'],
                        'public_ip': instance.get('PublicIpAddress', 'N/A'),
                        'launch_time': instance['LaunchTime']
                    })

            return instances

        except ClientError as e:
            print(f"❌ Error listing instances: {e}")
            return []


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 2025

@author: ramyalsaffar
"""
