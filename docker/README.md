# Docker Setup for Alignment Tax Experiments

This directory contains Docker configuration for containerizing alignment tax experiments.

## Files

- `Dockerfile`: Multi-stage Docker build configuration
- `docker-compose.yml`: Local development and testing setup
- `.dockerignore`: Excludes unnecessary files from build context

## Quick Start

### 1. Build the Image
```bash
# From project root
cd docker
docker-compose build
```

### 2. Run Container
```bash
# Start container
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Execute Commands
```bash
# Enter container
docker-compose exec alignment-tax bash

# Inside container - run experiment
python src/16-Execute.py

# Or run directly
docker-compose exec alignment-tax python src/16-Execute.py
```

### 4. Stop Container
```bash
docker-compose down
```

## Configuration

### Environment Variables
Set in `docker-compose.yml` or pass at runtime:

```yaml
environment:
  - ENVIRONMENT=aws          # 'local' or 'aws'
  - AWS_REGION=us-east-1
  - S3_BUCKET_NAME=alignment-tax-results
```

### Volume Mounts
For local development, code is mounted as volumes:

```yaml
volumes:
  - ../src:/app/src          # Source code
  - ../results:/app/results  # Results output
  - ../models:/app/models    # Model files
```

### Resource Limits
Adjust based on your hardware:

```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 16G
```

## Building for Production

### Optimize Image Size
```bash
# Build without cache
docker build --no-cache -t alignment-tax:latest -f docker/Dockerfile .

# Check image size
docker images alignment-tax
```

### Multi-platform Build
```bash
# For ARM64 (Apple Silicon) and AMD64
docker buildx build --platform linux/amd64,linux/arm64 \
    -t alignment-tax:latest -f docker/Dockerfile .
```

## AWS ECR Integration

### Push to ECR
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag alignment-tax:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/alignment-tax:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/alignment-tax:latest
```

### Pull from ECR
```bash
docker pull <account-id>.dkr.ecr.us-east-1.amazonaws.com/alignment-tax:latest
```

## Troubleshooting

### Build fails
- Check `requirements.txt` exists
- Verify base image is accessible
- Check `.dockerignore` isn't excluding needed files

### Container exits immediately
- Check `CMD` in Dockerfile
- Review logs: `docker-compose logs`
- Verify entry point script is executable

### Permission denied
- Check file permissions in mounted volumes
- Verify user ID mapping (using non-root user)

### Out of memory
- Increase memory limit in `docker-compose.yml`
- Check host system resources
- Reduce model context size in config

## Development Workflow

### 1. Local Development
```bash
# Make code changes in src/
# No rebuild needed (volume mounted)
docker-compose exec alignment-tax python src/16-Execute.py --test
```

### 2. Test Changes
```bash
# Quick test run
docker-compose exec alignment-tax python -c "from src.Pipeline import *; print('OK')"
```

### 3. Production Build
```bash
# Build production image (no volumes)
docker build -t alignment-tax:v03 -f docker/Dockerfile .

# Run production image
docker run alignment-tax:v03
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Build Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t alignment-tax:${{ github.sha }} -f docker/Dockerfile .

      - name: Push to ECR
        run: |
          aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
          docker tag alignment-tax:${{ github.sha }} ${{ secrets.ECR_REGISTRY }}/alignment-tax:latest
          docker push ${{ secrets.ECR_REGISTRY }}/alignment-tax:latest
```

## Best Practices

1. **Layer Caching**: Order Dockerfile commands from least to most frequently changing
2. **Multi-stage Builds**: Separate build and runtime dependencies
3. **Security**: Run as non-root user, scan for vulnerabilities
4. **Size**: Use slim base images, clean up in same layer
5. **Secrets**: Never bake secrets into images, use env vars or AWS Secrets Manager

## Health Checks

### Add to Dockerfile
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1
```

### Monitor Health
```bash
docker inspect --format='{{.State.Health.Status}}' alignment-tax-worker
```

## Useful Commands

```bash
# View container resources
docker stats alignment-tax-worker

# Execute arbitrary command
docker-compose exec alignment-tax bash -c "python --version"

# Copy files from container
docker cp alignment-tax-worker:/app/results ./results

# View container logs
docker-compose logs --tail=100 -f alignment-tax
```
