from logging import Logger
import re
import requests

from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
EXTRACT_URL_REGEX = r'https?://\S+|www\.\S+|\S+\.(com|org|net|edu|gov|io|co|ai|app)(/\S*)?'

class ScrapeService:
    def __init__(self, logger: Logger):
        self.logger = logger
        
    def extract_text_from_url(self, url):
        try:
            headers = {
                'User-Agent': USER_AGENT
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for script in soup(["script", "style", "header", "footer", "nav"]):
                script.extract()
                
            text = soup.get_text(separator=' ')
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            text = re.sub(r'\n+', '\n', text)
            text = re.sub(r'\s+', ' ', text)
            
            text = re.sub(EXTRACT_URL_REGEX, '', text)
            
            return text
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Cannot fetch webpage {e}")
            raise e
        except Exception as e:
            self.logger.error("Error processing content: {e}")
            raise e
