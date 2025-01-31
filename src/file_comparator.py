import pandas as pd
import yaml
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class FileComparator:
    @staticmethod
    def create_comparison_table(file1_content: str, file2_content: str, file1_repository: str, file2_repository: str) -> str:
        # Debug logging
        logger.debug("File 1 content:")
        logger.debug(file1_content)
        logger.debug("File 2 content:")
        logger.debug(file2_content)
        
        try:
            # Parse YAML content
            data1 = yaml.safe_load(file1_content)
            data2 = yaml.safe_load(file2_content)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {str(e)}")
            raise
        
        # Convert data to a format suitable for comparison
        html_output = []
        
        # Get all unique server names from both files
        all_servers = {s['serverName'] for s in data1['servers']}.union(
            {s['serverName'] for s in data2['servers']}
        )
        
        
        # Create tables for each server
        for server_name in sorted(all_servers):
            server1 = next((s for s in data1['servers'] if s['serverName'] == server_name), None)
            server2 = next((s for s in data2['servers'] if s['serverName'] == server_name), None)
            
            bars1 = {b['name']: b['version'] for b in server1['bars']} if server1 else {}
            bars2 = {b['name']: b['version'] for b in server2['bars']} if server2 else {}
            all_bars = set(bars1.keys()).union(set(bars2.keys()))
            
            # Start server section
            html_output.append(f'h3. {server_name}')
            
            # Create bar table for this server
            html_output.append(f'||Bar||{file1_repository}||{file2_repository}||')
            
            for bar_name in sorted(all_bars):
                version1 = bars1.get(bar_name, ' ')
                version2 = bars2.get(bar_name, ' ')
                
                if version1 != version2:
                    html_output.append(
                        f'|{bar_name}|{{color:red}}{version1}{{color}}|{{color:red}}{version2}{{color}}|'
                    )
                else:
                    html_output.append(
                        f'|{bar_name}|{version1}|{version2}|'
                    )
                    
        return '\n'.join(html_output)