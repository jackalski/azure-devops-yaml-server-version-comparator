# Azure DevOps YAML File Comparator

A Python tool that compares YAML files between Azure DevOps repositories and publishes the comparison results to a Confluence page. The tool is specifically designed to compare server and bar configurations across different environments.

## Features

- Fetches YAML files from different Azure DevOps repositories
- Compares server and bar configurations
- Highlights version differences in red
- Groups results by server
- Publishes formatted results to Confluence
- Supports SSL verification toggle for internal certificates
- Auto-generates default configuration file

## Prerequisites

- Python 3.10 or higher
- Azure DevOps Personal Access Token with read permissions
- Confluence Personal Access Token with write permissions

## Obtaining Access Tokens

### Azure DevOps PAT

1. Go to Azure DevOps and click on your profile picture
2. Select "Personal access tokens"
3. Click "New Token"
4. Configure the token:
   - Name: Give it a descriptive name (e.g., "YAML File Comparator")
   - Organization: Select your organization
   - Expiration: Choose an expiration date
   - Scopes: Select "Read" under "Code"
5. Click "Create" and copy the token value

### Confluence PAT

1. Log in to your Confluence instance
2. Go to Profile Settings (click on your profile picture)
3. Select "Security" or "Personal access tokens"
4. Click "Create token"
5. Configure the token:
   - Token name: Give it a descriptive name
   - Permissions: Select "Read" and "Write" for Space and Page
   - Expiration: Set an expiration date
6. Click "Create" and copy the token value

Note: Store these tokens securely and never commit them to version control.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

On first run, the tool will automatically create a `config.yaml` file with default values. Edit this file with your actual configuration:

```yaml
azure_devops:
organization: "your-org"
project: "your-project"
pat: "your-azure-pat"
file1:
repository: "repo1-id"
path: "path/to/first/file.yaml"
branch: "main"
file2:
repository: "repo2-id"
path: "path/to/second/file.yaml"
branch: "main"
confluence:
base_url: "https://your-confluence-instance"
space_key: "your-space-key"
page_id: "your-page-id"
pat: "your-confluence-pat"
verify_ssl: false # Set to true for production environments

## Usage

Run the script:

```bash
python src/main.py
```

The script will:
1. Create default configuration file if none exists
2. Load configuration from config.yaml
3. Fetch YAML files from Azure DevOps repositories
4. Compare server and bar versions
5. Create a formatted comparison table
6. Update the specified Confluence page

## Output Format

The comparison results will be published to Confluence with:
- Server names as section headers
- Tables showing bar versions from both files
- Version differences highlighted in red
- Repository and file path information

## Error Handling

The script includes comprehensive error handling and logging:
- Configuration loading errors
- Azure DevOps connection/file fetch issues
- YAML parsing errors
- Confluence update failures

Logs are output to console with timestamps and log levels.

## Security Notes

- Store PATs securely and never commit them to version control
- Use environment variables or secure vaults in production
- Enable SSL verification in production environments
- Rotate PATs regularly according to your security policies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 