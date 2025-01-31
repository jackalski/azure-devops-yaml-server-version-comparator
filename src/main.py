import os
import yaml
import logging
import sys
from config import AzureDevOpsConfig, ConfluenceConfig, FileLocation
from azure_devops_client import AzureDevOpsClient
from confluence_client import ConfluenceClient
from file_comparator import FileComparator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_default_config(config_path: str = 'config.yaml'):
    """Create a default configuration file with dummy values"""
    default_config = {
        'azure_devops': {
            'organization': 'your-org',
            'project': 'your-project',
            'pat': 'your-azure-pat',
            'file1': {
                'repository': 'repo1-id',
                'path': 'path/to/first/file.yaml',
                'branch': 'main'
            },
            'file2': {
                'repository': 'repo2-id',
                'path': 'path/to/second/file.yaml',
                'branch': 'main'
            }
        },
        'confluence': {
            'base_url': 'https://your-confluence-instance',
            'space_key': 'your-space-key',
            'page_id': 'your-page-id',
            'pat': 'your-confluence-pat',
            'verify_ssl': False
        }
    }
    
    try:
        with open(config_path, 'w') as file:
            yaml.dump(default_config, file, default_flow_style=False)
        logger.info(f"Created default configuration file at {config_path}")
    except Exception as e:
        logger.error(f"Failed to create default configuration: {str(e)}")
        raise

def load_config(config_path: str = 'config.yaml'):
    """Load configuration from YAML file"""
    if not os.path.exists(config_path):
        logger.warning(f"Configuration file not found at {config_path}")
        create_default_config(config_path)
        logger.info("Please update the configuration file with your values and run again")
        sys.exit(1)
        
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        azure_config = AzureDevOpsConfig(
            organization=config['azure_devops']['organization'],
            project=config['azure_devops']['project'],
            pat=config['azure_devops']['pat'],
            file1=FileLocation(**config['azure_devops']['file1']),
            file2=FileLocation(**config['azure_devops']['file2'])
        )
        
        confluence_config = ConfluenceConfig(
            base_url=config['confluence']['base_url'],
            space_key=config['confluence']['space_key'],
            page_id=config['confluence']['page_id'],
            pat=config['confluence']['pat']
        )
        
        return azure_config, confluence_config
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise

def main():
    try:
        logger.info("Loading configuration...")
        azure_config, confluence_config = load_config()
        
        logger.info("Initializing clients...")
        azure_client = AzureDevOpsClient(azure_config)
        confluence_client = ConfluenceClient(confluence_config)

        logger.info("Fetching files from Azure DevOps...")
        file1_content = azure_client.get_file_content(azure_config.file1)
        file2_content = azure_client.get_file_content(azure_config.file2)
        
        logger.info("Creating comparison table...")
        comparison_table = FileComparator.create_comparison_table(file1_content=file1_content, file2_content=file2_content, file1_repository=azure_config.file1.repository, file2_repository=azure_config.file2.repository)
        
        logger.info("Creating Confluence content...")
        confluence_content = f"""
h1. File Comparison Results
Comparison between:
* Repository: {azure_config.file1.repository}, Path: {azure_config.file1.path}, Branch: {azure_config.file1.branch}
* Repository: {azure_config.file2.repository}, Path: {azure_config.file2.path}, Branch: {azure_config.file2.branch}

----
{comparison_table}
        """
        
        logger.info("Updating Confluence page...")
        confluence_client.update_page(confluence_content)
        
        logger.info("Successfully updated Confluence page with comparison results")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main() 