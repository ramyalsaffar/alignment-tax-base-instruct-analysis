# AWS Infrastructure Setup

This directory contains AWS infrastructure code for running alignment tax experiments at scale.

## Components

### 1. S3Handler (`s3_handler.py`)
- Uploads results and logs to S3
- Downloads previous results
- Lists all experiment runs
- Automatic bucket creation

### 2. SecretsHandler (`secrets_handler.py`)
- Retrieves OpenAI API key from AWS Secrets Manager
- Secure credential management
- No hardcoded keys in code

### 3. EC2Manager (`ec2_setup.py`)
- Launches EC2 instances for experiments
- Configures security groups
- Manages instance lifecycle
- Recommended instance: t3.xlarge (4 vCPUs, 16GB RAM)

### 4. Configuration (`config_aws.py`)
- Environment detection
- Path management for AWS vs local
- AWS service configuration

## Setup Instructions

### Prerequisites
1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Python 3.11+

### Step 1: Configure AWS CLI
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1
# Default output format: json
```

### Step 2: Create IAM Role
The EC2 instances need an IAM role with permissions for:
- S3 (read/write to results bucket)
- Secrets Manager (read OpenAI API key)
- CloudWatch Logs (optional, for logging)

```bash
# Create IAM role (from aws directory)
python create_iam_role.py
```

### Step 3: Store OpenAI API Key in Secrets Manager
```bash
aws secretsmanager create-secret \
    --name alignment-tax/openai-api-key \
    --description "OpenAI API key for alignment tax experiments" \
    --secret-string "your-openai-api-key-here"
```

### Step 4: Create S3 Bucket
```bash
aws s3 mb s3://alignment-tax-results --region us-east-1
```

### Step 5: Launch EC2 Instance
```python
from aws import EC2Manager

ec2 = EC2Manager(region='us-east-1')
instance_id = ec2.launch_instance(
    instance_type='t3.xlarge',
    instance_name='alignment-tax-experiment'
)
```

### Step 6: Deploy Code to EC2
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@<instance-ip>

# Clone repository
git clone https://github.com/your-username/alignment-tax-base-instruct-analysis.git
cd alignment-tax-base-instruct-analysis

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-aws.txt

# Run experiment
ENVIRONMENT=aws python src/16-Execute.py
```

## Docker Deployment

### Build Image
```bash
cd docker
docker-compose build
```

### Run Locally (Test)
```bash
docker-compose up -d
docker-compose exec alignment-tax bash
# Inside container:
python src/16-Execute.py
```

### Push to ECR (Optional)
```bash
# Create ECR repository
aws ecr create-repository --repository-name alignment-tax

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag alignment-tax:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/alignment-tax:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/alignment-tax:latest
```

## Cost Estimates

### EC2 (t3.xlarge)
- On-Demand: ~$0.1664/hour
- 12-hour experiment: ~$2.00

### S3 Storage
- First 50 TB: $0.023/GB/month
- 1GB results: ~$0.023/month

### Secrets Manager
- $0.40/secret/month

### Total per Run
- **~$2-3 per full experiment** (excluding API costs)

## Environment Variables

Set these in your environment or `.env` file:

```bash
# Required
ENVIRONMENT=aws
AWS_REGION=us-east-1

# Optional (have defaults)
S3_BUCKET_NAME=alignment-tax-results
SECRETS_OPENAI_KEY_NAME=alignment-tax/openai-api-key
EC2_INSTANCE_TYPE=t3.xlarge
```

## Security Best Practices

1. **Never commit credentials**: Use Secrets Manager
2. **Restrict security groups**: Limit SSH access to your IP
3. **Use IAM roles**: Don't use access keys on EC2
4. **Enable encryption**: S3 bucket encryption enabled by default
5. **Regular cleanup**: Terminate instances after experiments

## Troubleshooting

### Issue: Can't access S3
- Check IAM role permissions
- Verify bucket name and region

### Issue: Can't retrieve API key
- Verify Secrets Manager secret exists
- Check IAM permissions for secretsmanager:GetSecretValue

### Issue: EC2 launch fails
- Check security group exists
- Verify AMI availability in your region
- Ensure IAM role exists

## Monitoring

### Check experiment progress
```bash
# View CloudWatch logs (if configured)
aws logs tail /aws/ec2/alignment-tax --follow

# Check S3 for results
aws s3 ls s3://alignment-tax-results/runs/

# Check instance status
aws ec2 describe-instances --filters "Name=tag:Project,Values=alignment-tax"
```

## Cleanup

### After experiment completes
```bash
# Stop instance (preserves for later use)
aws ec2 stop-instances --instance-ids <instance-id>

# Or terminate instance (deletes it)
aws ec2 terminate-instances --instance-ids <instance-id>
```

## Support

For issues or questions:
- Check AWS CloudWatch logs
- Review EC2 instance system logs
- Verify IAM permissions
