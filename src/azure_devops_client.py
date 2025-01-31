import base64
import os
from azure.devops.connection import Connection
from azure.devops.v7_1.git import GitClient, GitVersionDescriptor, GitItem, GitItemRequestData
from msrest.authentication import BasicAuthentication
from config import FileLocation

class AzureDevOpsClient:
    def __init__(self, config):
        self.config = config
        self.client = self._create_client()
        
    def _create_client(self):
        organization_url = f"https://dev.azure.com/{self.config.organization}"
        credentials = BasicAuthentication('', self.config.pat)
        connection = Connection(base_url=organization_url, creds=credentials)
        return connection.clients.get_git_client()
        
    def get_file_content(self, file_location: FileLocation) -> str:
        fileOutput = ""
        try:
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
            with open(os.devnull, 'wb') as f:
                for x in content:
                    fileOutput += x.decode('utf-8')

            return fileOutput
        except Exception as e:
            raise Exception(f"Error fetching file {file_location.path} from repo {file_location.repository}: {str(e)}") 