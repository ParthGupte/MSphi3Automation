import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import time
import re
from bs4 import BeautifulSoup


def get_page_content(url, timeout=10, retries=3, delay=1):
    """
    Fetch the entire contents of a webpage and return as a string.
    
    Args:
        url (str): The URL to fetch
        timeout (int): Request timeout in seconds (default: 10)
        retries (int): Number of retry attempts (default: 3)
        delay (int): Delay between retries in seconds (default: 1)
    
    Returns:
        str: The complete HTML content of the page
        
    Raises:
        RequestException: If the request fails after all retries
    """
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Common headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    last_exception = None
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            # Return the text content
            return response.text
            
        except (ConnectionError, Timeout) as e:
            last_exception = e
            if attempt < retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise RequestException(f"Failed to fetch {url} after {retries} attempts: {e}")
                
        except RequestException as e:
            raise RequestException(f"Error fetching {url}: {e}")
    
    # This shouldn't be reached, but just in case
    if last_exception:
        raise last_exception

def clean_html_to_text(html_content, preserve_structure=True):
    """
    Clean HTML content and extract only readable text suitable for LLM processing.
    
    Args:
        html_content (str): Raw HTML content
        preserve_structure (bool): Whether to preserve some structure with line breaks
    
    Returns:
        str: Clean text content suitable for LLM
    """
    if not html_content:
        return ""
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements completely
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    
    # Remove common navigation and footer elements
    for element in soup.find_all(['nav', 'footer', 'header']):
        element.decompose()
    
    # Remove elements with common non-content classes/ids
    unwanted_selectors = [
        '[class*="nav"]', '[class*="menu"]', '[class*="sidebar"]',
        '[class*="footer"]', '[class*="header"]', '[class*="advertisement"]',
        '[class*="ad-"]', '[class*="popup"]', '[class*="modal"]',
        '[id*="nav"]', '[id*="menu"]', '[id*="sidebar"]',
        '[id*="footer"]', '[id*="header"]', '[id*="ad"]'
    ]
    
    for selector in unwanted_selectors:
        for element in soup.select(selector):
            element.decompose()
    
    if preserve_structure:
        # Add line breaks for structural elements
        for tag in soup.find_all(['p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
            tag.append('\n')
        
        # Add extra line breaks for major sections
        for tag in soup.find_all(['h1', 'h2', 'h3', 'article', 'section']):
            tag.append('\n')
    
    # Extract text
    text = soup.get_text()
    
    # Clean up the text
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove excessive line breaks but preserve paragraph structure
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Remove empty lines at the beginning and end
    text = text.strip()
    
    return text

def get_clean_page_text(url, preserve_structure=True, timeout=10, retries=3, delay=1):
    """
    Fetch a webpage and return only the clean text content suitable for LLM processing.
    
    Args:
        url (str): The URL to fetch
        preserve_structure (bool): Whether to preserve some structure with line breaks
        timeout (int): Request timeout in seconds (default: 10)
        retries (int): Number of retry attempts (default: 3)
        delay (int): Delay between retries in seconds (default: 1)
    
    Returns:
        str: Clean text content of the webpage
        
    Raises:
        RequestException: If the request fails after all retries
    """
    # Get the raw HTML content
    html_content = get_page_content(url, timeout, retries, delay)
    
    # Clean and extract text
    clean_text = clean_html_to_text(html_content, preserve_structure)
    
    return clean_text

# Example usage


# print(r" Image Auto-regressive (AR) models have emerged as a powerful paradigm of visual generative models. Despite their promising performance, they suffer from slow generation speed due to the large number of sampling steps required. Although Distilled Decoding 1 (DD1) was recently proposed to enable few-step sampling for image AR models, it still incurs significant performance degradation in the one-step setting, and relies on a pre-defined mapping that limits its flexibility. In this work, we propose a new method, Distilled Decoding 2 (DD2), to further advances the feasibility of one-step sampling for image AR models. Unlike DD1, DD2 does not without rely on a pre-defined mapping. We view the original AR model as a teacher model which provides the ground truth conditional score in the latent embedding space at each token position. Based on this, we propose a novel \emph{conditional score distillation loss} to train a one-step generator. Specifically, we train a separate network to predict the conditional score of the generated distribution and apply score distillation at every token position conditioned on previous tokens. Experimental results show that DD2 enables one-step sampling for image AR models with an minimal FID increase from 3.40 to 5.43 on ImageNet-256. Compared to the strongest baseline DD1, DD2 reduces the gap between the one-step sampling and original AR model by 67\%, with up to 12.3$\times$ training speed-up simultaneously. DD2 takes a significant step toward the goal of one-step AR generation, opening up new possibilities for fast and high-quality AR modeling. Code is available at https://github.com/imagination-research/Distilled-Decoding-2." in get_page_content(r"https://neurips.cc/virtual/2025/loc/san-diego/papers.html?filter=topic&search=Computer+Vision-%3EImage+and+Video+Generation&layout=detail"))