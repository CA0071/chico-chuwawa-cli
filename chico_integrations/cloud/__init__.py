"""
Cloud Provider Integrations
AWS, GCP, and Azure basic integrations
"""

from typing import Dict, Any, List, Optional
from ..base import BaseIntegration, IntegrationStatus


class AWSIntegration(BaseIntegration):
    """AWS integration for basic service management"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("AWS", config)
        self.s3_client = None
        self.ec2_client = None
    
    def connect(self) -> bool:
        """Connect to AWS"""
        try:
            import boto3
            
            aws_access_key = self.config.get('aws_access_key_id')
            aws_secret_key = self.config.get('aws_secret_access_key')
            region = self.config.get('region', 'us-east-1')
            
            if aws_access_key and aws_secret_key:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region
                )
                self.ec2_client = boto3.client(
                    'ec2',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region
                )
            else:
                # Use default credentials (from environment or ~/.aws/credentials)
                self.s3_client = boto3.client('s3', region_name=region)
                self.ec2_client = boto3.client('ec2', region_name=region)
            
            # Test connection
            self.s3_client.list_buckets()
            self.status = IntegrationStatus.HEALTHY
            return True
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Check AWS connection health"""
        if not self.s3_client:
            return {"status": "unhealthy", "message": "Not connected"}
        
        try:
            self.s3_client.list_buckets()
            self.status = IntegrationStatus.HEALTHY
            return {"status": "healthy", "provider": "AWS"}
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return {"status": "unhealthy", "error": str(e)}
    
    def get_info(self) -> Dict[str, Any]:
        """Get AWS account information"""
        if not self.s3_client:
            return {"error": "Not connected"}
        
        try:
            import boto3
            sts_client = boto3.client('sts')
            identity = sts_client.get_caller_identity()
            
            return {
                "account_id": identity.get('Account'),
                "user_arn": identity.get('Arn'),
                "region": self.config.get('region', 'us-east-1')
            }
        except Exception as e:
            return {"error": str(e)}
    
    def list_s3_buckets(self) -> List[Dict[str, Any]]:
        """List S3 buckets"""
        if not self.s3_client:
            return []
        
        try:
            response = self.s3_client.list_buckets()
            return [{
                'name': bucket['Name'],
                'created': str(bucket['CreationDate'])
            } for bucket in response.get('Buckets', [])]
        except Exception as e:
            return [{"error": str(e)}]
    
    def list_ec2_instances(self) -> List[Dict[str, Any]]:
        """List EC2 instances"""
        if not self.ec2_client:
            return []
        
        try:
            response = self.ec2_client.describe_instances()
            instances = []
            for reservation in response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    instances.append({
                        'id': instance['InstanceId'],
                        'type': instance['InstanceType'],
                        'state': instance['State']['Name'],
                        'launch_time': str(instance.get('LaunchTime', 'Unknown'))
                    })
            return instances
        except Exception as e:
            return [{"error": str(e)}]


class GCPIntegration(BaseIntegration):
    """Google Cloud Platform integration"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("GCP", config)
        self.storage_client = None
    
    def connect(self) -> bool:
        """Connect to GCP"""
        try:
            from google.cloud import storage
            
            credentials_path = self.config.get('credentials_path')
            if credentials_path:
                import os
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            
            self.storage_client = storage.Client()
            
            # Test connection by listing buckets (will fail if no permissions)
            list(self.storage_client.list_buckets(max_results=1))
            self.status = IntegrationStatus.HEALTHY
            return True
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Check GCP connection health"""
        if not self.storage_client:
            return {"status": "unhealthy", "message": "Not connected"}
        
        try:
            list(self.storage_client.list_buckets(max_results=1))
            self.status = IntegrationStatus.HEALTHY
            return {"status": "healthy", "provider": "GCP"}
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return {"status": "unhealthy", "error": str(e)}
    
    def get_info(self) -> Dict[str, Any]:
        """Get GCP project information"""
        if not self.storage_client:
            return {"error": "Not connected"}
        
        return {
            "project": self.storage_client.project
        }
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """List GCS buckets"""
        if not self.storage_client:
            return []
        
        try:
            buckets = self.storage_client.list_buckets()
            return [{
                'name': bucket.name,
                'created': str(bucket.time_created),
                'location': bucket.location
            } for bucket in buckets]
        except Exception as e:
            return [{"error": str(e)}]


class AzureIntegration(BaseIntegration):
    """Microsoft Azure integration"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("Azure", config)
        self.blob_service_client = None
    
    def connect(self) -> bool:
        """Connect to Azure"""
        try:
            from azure.storage.blob import BlobServiceClient
            
            connection_string = self.config.get('connection_string')
            account_url = self.config.get('account_url')
            
            if connection_string:
                self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            elif account_url:
                self.blob_service_client = BlobServiceClient(account_url=account_url)
            else:
                return False
            
            # Test connection
            list(self.blob_service_client.list_containers(max_results=1))
            self.status = IntegrationStatus.HEALTHY
            return True
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Check Azure connection health"""
        if not self.blob_service_client:
            return {"status": "unhealthy", "message": "Not connected"}
        
        try:
            list(self.blob_service_client.list_containers(max_results=1))
            self.status = IntegrationStatus.HEALTHY
            return {"status": "healthy", "provider": "Azure"}
        except Exception as e:
            self.status = IntegrationStatus.UNHEALTHY
            return {"status": "unhealthy", "error": str(e)}
    
    def get_info(self) -> Dict[str, Any]:
        """Get Azure account information"""
        if not self.blob_service_client:
            return {"error": "Not connected"}
        
        return {
            "account_name": self.blob_service_client.account_name,
            "url": self.blob_service_client.url
        }
    
    def list_containers(self) -> List[Dict[str, Any]]:
        """List Blob containers"""
        if not self.blob_service_client:
            return []
        
        try:
            containers = self.blob_service_client.list_containers()
            return [{
                'name': container['name'],
                'last_modified': str(container.get('last_modified', 'Unknown'))
            } for container in containers]
        except Exception as e:
            return [{"error": str(e)}]
