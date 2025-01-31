import requests
import json
from atlassian import Confluence
import urllib3
import logging

logger = logging.getLogger(__name__)

class ConfluenceClient:
    def __init__(self, config):
        self.config = config
        if not self.config.verify_ssl:
            # Disable SSL verification warnings
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.confluence = Confluence(
            url=self.config.base_url,
            token=self.config.pat,
            verify_ssl=self.config.verify_ssl
        )
        
    def update_page(self, content):
        try:            
            self.confluence.update_page(
                page_id=self.config.page_id,
                title=self.confluence.get_page_by_id(self.config.page_id)['title'],
                body=content,
                type='page',
                representation='wiki'
            )
        except Exception as e:
            logger.error(f"Error updating Confluence page: {str(e)}")
            raise 