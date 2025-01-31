from dataclasses import dataclass
from typing import Optional

@dataclass
class FileLocation:
    repository: str
    path: str
    branch: str = 'main'

@dataclass
class AzureDevOpsConfig:
    organization: str
    project: str
    pat: str
    file1: FileLocation
    file2: FileLocation
    
@dataclass
class ConfluenceConfig:
    base_url: str
    space_key: str
    page_id: str
    pat: str
    verify_ssl: bool = False