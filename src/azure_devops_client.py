import base64
import os
from azure.devops.connection import Connection
from azure.devops.v7_1.git import GitClient, GitVersionDescriptor, GitItem
from msrest.authentication import BasicAuthentication
from config import FileLocation
import logging

logger = logging.getLogger(__name__)

class AzureDevOpsClient:
    def __init__(self, config):
        self.config = config
        self.client = self._create_client()
        
    def _create_client(self):
        organization_url = f"https://dev.azure.com/{self.config.organization}"
        credentials = BasicAuthentication('', self.config.pat)
        connection = Connection(base_url=organization_url, creds=credentials)
        return connection.clients.get_git_client()
        
    def get_file_content(self, file_location: FileLocation) -> dict:
        try:
            if file_location.path.endswith('.yaml'):
                return {file_location.path: self._get_single_file(file_location)}
            else:
                return self._get_directory_files(file_location)
        except Exception as e:
            raise Exception(f"Error fetching from {file_location.repository}: {str(e)}")
            
    def _get_single_file(self, file_location: FileLocation) -> str:
        version_descriptor = GitVersionDescriptor(
            version=file_location.branch,
            version_type="branch"
        )
        
        content = self.client.get_item_content(
            repository_id=file_location.repository,
            path=file_location.path,
            project=self.config.project,
            version_descriptor=version_descriptor,
            include_content=True,
            download=True
        )
        
        return ''.join(chunk.decode('utf-8') for chunk in content)
        
    def _get_directory_files(self, file_location: FileLocation) -> dict:
        version_descriptor = GitVersionDescriptor(
            version=file_location.branch,
            version_type="branch"
        )
        
        try:
            # Get items using get_items with scope path
            items = self.client.get_items(
                repository_id=file_location.repository,
                project=self.config.project,
                scope_path=file_location.path,  # Use scope_path instead
                recursion_level="Full",         # Use recursion_level parameter
                version_descriptor=version_descriptor
            )
            
            yaml_files = {}
            for item in items:
                if item.path.endswith('.yaml'):
                    logger.info(f"Found YAML file: {item.path}")
                    content = self._get_single_file(FileLocation(
                        repository=file_location.repository,
                        path=item.path,
                        branch=file_location.branch
                    ))
                    yaml_files[item.path] = content
                    
            return yaml_files
            
        except Exception as e:
            raise Exception(f"Error listing files in {file_location.path}: {str(e)}") 