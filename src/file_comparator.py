import pandas as pd
import yaml
import logging
import os
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class FileComparator:
    @staticmethod
    def create_comparison_table(file1_content: dict, file2_content: dict, file1_repository: str, file2_repository: str) -> str:
        # Check if we're comparing single files or directories
        is_single_file = len(file1_content) == 1 and len(file2_content) == 1 and \
                        list(file1_content.keys())[0].endswith('.yaml')
        
        if is_single_file:
            # Single file comparison - group by servers
            content1 = list(file1_content.values())[0]
            content2 = list(file2_content.values())[0]
            
            try:
                data1 = yaml.safe_load(content1) if content1 else {'servers': []}
                data2 = yaml.safe_load(content2) if content2 else {'servers': []}
            except yaml.YAMLError as e:
                logger.error(f"YAML parsing error: {str(e)}")
                raise
                
            return FileComparator._create_server_comparison(data1, data2)
        else:
            # Directory comparison - group by files
            return FileComparator._create_directory_comparison(file1_content, file2_content)
    
    @staticmethod
    def _create_server_comparison(data1: dict, data2: dict) -> str:
        # Get all unique server names
        all_servers = {s['serverName'] for s in data1.get('servers', [])}.union(
            {s['serverName'] for s in data2.get('servers', [])}
        )
        
        all_tables = []
        
        for server_name in sorted(all_servers):
            server1 = next((s for s in data1.get('servers', []) if s['serverName'] == server_name), None)
            server2 = next((s for s in data2.get('servers', []) if s['serverName'] == server_name), None)
            
            # Create table for this server
            table = f"h2. Server: {server_name}\n"
            table += "||Bar||File 1 Version||File 2 Version||\n"
            
            bars1 = {b['name']: b['version'] for b in server1['bars']} if server1 else {}
            bars2 = {b['name']: b['version'] for b in server2['bars']} if server2 else {}
            all_bars = set(bars1.keys()).union(set(bars2.keys()))
            
            for bar_name in sorted(all_bars):
                version1 = bars1.get(bar_name, 'N/A')
                version2 = bars2.get(bar_name, 'N/A')
                
                if version1 != version2:
                    version1 = f"{{color:red}}{version1}{{color}}"
                    version2 = f"{{color:red}}{version2}{{color}}"
                
                table += f"|{bar_name}|{version1}|{version2}|\n"
            
            all_tables.append(table)
        
        return "\n----\n".join(all_tables)
    
    @staticmethod
    def _create_directory_comparison(file1_content: dict, file2_content: dict) -> str:
        all_tables = []
        
        # Extract filenames and environments from paths
        files1 = {os.path.basename(path): (content, os.path.basename(os.path.dirname(path))) 
                 for path, content in file1_content.items()}
        files2 = {os.path.basename(path): (content, os.path.basename(os.path.dirname(path))) 
                 for path, content in file2_content.items()}
        
        # Get all unique filenames
        all_filenames = set(files1.keys()).union(set(files2.keys()))
        
        for filename in sorted(all_filenames):
            logger.info(f"Comparing file: {filename}")
            content1, env1 = files1.get(filename, ('', 'N/A'))
            content2, env2 = files2.get(filename, ('', 'N/A'))
            
            try:
                data1 = yaml.safe_load(content1) if content1 else {'servers': []}
                data2 = yaml.safe_load(content2) if content2 else {'servers': []}
            except yaml.YAMLError as e:
                logger.error(f"YAML parsing error for {filename}: {str(e)}")
                continue
            
            # Create table for this file
            table = f"h2. Comparing {filename}\n"
            table += f"||Server||Bar||{env1} Version||{env2} Version||\n"
            
            # Get all unique server names
            all_servers = {s['serverName'] for s in data1.get('servers', [])}.union(
                {s['serverName'] for s in data2.get('servers', [])}
            )
            
            for server_name in sorted(all_servers):
                server1 = next((s for s in data1.get('servers', []) if s['serverName'] == server_name), None)
                server2 = next((s for s in data2.get('servers', []) if s['serverName'] == server_name), None)
                
                bars1 = {b['name']: b['version'] for b in server1['bars']} if server1 else {}
                bars2 = {b['name']: b['version'] for b in server2['bars']} if server2 else {}
                all_bars = set(bars1.keys()).union(set(bars2.keys()))
                
                for bar_name in sorted(all_bars):
                    version1 = bars1.get(bar_name, 'N/A')
                    version2 = bars2.get(bar_name, 'N/A')
                    
                    if version1 != version2:
                        version1 = f"{{color:red}}{version1}{{color}}"
                        version2 = f"{{color:red}}{version2}{{color}}"
                    
                    table += f"|{server_name}|{bar_name}|{version1}|{version2}|\n"
            
            all_tables.append(table)
        
        return "\n----\n".join(all_tables)