# Web Crawler Project


## Introduction
This Web Crawler is a Python-based tool designed to efficiently navigate and catalog web pages within a specified domain. Built with attention to software design and structure, this crawler emphasizes efficient resource management, user-friendliness, and robust data collection.


## Features
- Domain-Specific Crawling: Focuses on a single domain, ensuring comprehensive coverage of the targeted website without straying into external sites.
- Concurrency Control: Manages multiple requests simultaneously, optimizing the crawling process while maintaining system stability.
- Dynamic URL Filtering: Excludes undesired content types and file extensions, focusing on relevant web pages.
- Robust Logging: Detailed logging of crawling activities, aiding in monitoring and debugging.
- Customizable Settings: Easy-to-adjust settings for concurrency limits, start URLs, and more.
- Asynchronous Design: Utilizes asynchronous programming for efficient network operations.


## Setup Instructions
### Prerequisites
- Python 3.8 or higher
- aiohttp
- bs4 (BeautifulSoup)
- fake_useragent
- aiohttp_retry

### Installation
1. Clone the repository to your local machine.
```bash
git clone https://github.com/elsbrd/WebCrawler.git
```
2. Navigate to the project directory.
```bash
cd WebCrawler/
```
3. Create a python virtual environment and activate it.
```bash
python3 -m venv venv
source venv/bin/activate
```
4. Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```


## Usage
To start the web crawler, use the following command:
```bash
python main.py [root_url] --concurrency [number]
```
- `root_url`: The starting URL for the crawler (e.g., https://www.example.com).
- `--concurrency`: Optional. The number of concurrent requests (default is 5).


## Logging
Logs are stored in the core/logs directory. These logs provide detailed information about the crawling process, including visited URLs and discovered links.


## Future Improvements
The development and enhancement of this Web Crawler are ongoing processes, and we are always looking to make it more efficient and respectful of web standards. Key areas of future improvements include:
### Processing `robots.txt` Files
- Respect Website Guidelines: Implementing the ability to read and adhere to the rules specified in `robots.txt` files on websites. This feature will ensure that the crawler respects the website owner's guidelines on what should and should not be crawled, thereby promoting ethical crawling practices.
- Efficient Crawling: By following `robots.txt` directives, the crawler can avoid unnecessary requests to disallowed paths, improving efficiency and reducing the load on both the crawler and the target servers.

### Handling `nofollow` Links
- Acknowledging `nofollow` Attributes: Enhancing the crawler to recognize and respect `nofollow` attributes in links. This improvement will ensure that the crawler does not follow links that are explicitly marked as `nofollow` by the website owners, aligning with best practices in web crawling and SEO.
- Selective Crawling: With `nofollow` handling, the crawler can be more selective in the links it chooses to follow, focusing efforts on the most relevant and permitted content, thereby improving the overall quality and relevance of the crawled data.