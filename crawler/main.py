import asyncio
from typing import Set
from urllib.parse import unquote, urldefrag, urljoin, urlparse

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from core.logging import setup_logger
from crawler.constants import UNDESIRED_EXTENSIONS, UNDESIRED_SCHEMES, StatusCode
from crawler.constants.enums import ContentType
from crawler.utils import AtomicSet

logger = setup_logger(__name__)


class WebCrawler:
    def __init__(self, root_url: str, concurrency_limit: int = 5):
        """
        Initialize the WebCrawler object.

        Args:
            root_url (str): The root URL to start crawling from.
            concurrency_limit (int): The maximum number of concurrent requests.
        """

        self.root_url = root_url
        self.root_netloc = urlparse(root_url).netloc

        self._visited_urls = AtomicSet()
        self._semaphore = asyncio.Semaphore(concurrency_limit)

    async def start(self):
        """
        Start the web crawling process.
        """

        logger.info(f"Crawling process is started for {self.root_url}")
        await self.crawl(self.root_url)
        logger.info(f"Crawling process is finished.")

    async def crawl(self, url: str):
        """
        Recursively crawl pages starting from the given URL.

        Args:
            url (str): The URL to start crawling from.
        """

        if await self._visited_urls.contains(url):
            return  # Skip if the URL has already been visited

        logger.info(f"Visiting: {url}")
        await self._visited_urls.add(url)

        html = await self._fetch_url(url)
        if html:
            page_urls = self._extract_urls(html)
            logger.info(
                f"Done {url}. {len(page_urls)} URLs found. " + ", ".join(page_urls)
            )

            tasks = [
                self.crawl(p_url)
                for p_url in page_urls
                if not self._is_undesired_url(p_url)
            ]
            await asyncio.gather(*tasks)

    async def _fetch_url(self, url: str):
        """
        Fetch the content of a URL.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The fetched HTML content, or None if the fetch fails.
        """

        async with self._semaphore:
            try:
                async with self._create_session() as session:
                    async with session.get(url) as response:
                        if (
                            ContentType.TEXT_HTML
                            in response.headers.get("Content-Type", "")
                            and response.status == StatusCode.HTTP_200_OK
                        ):
                            return await response.text()
            except (
                aiohttp.ClientError,
                aiohttp.http_exceptions.HttpProcessingError,
            ) as e:
                logger.error(f"Error fetching {url}: {e}")
            finally:
                await session.close()

    def _extract_urls(self, html: str) -> Set[str]:
        """
        Extract URLs from the given HTML content.

        Args:
            html (str): The HTML content to parse.

        Returns:
            Set[str]: A set of extracted URLs.
        """

        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for link in soup.find_all("a"):
            href = link.get("href")
            href = self._clean_href(href)
            if href:
                full_url = urljoin(self.root_url, href)

                if self.__is_same_domain_url(full_url):
                    links.add(full_url)

        return links

    @staticmethod
    def _create_session() -> RetryClient:
        """
        Create a session with retry logic and custom headers.

        This method configures a RetryClient session with exponential retry logic,
        a custom user agent, and a specified timeout.

        Returns:
            RetryClient: A configured instance of RetryClient for making HTTP requests.
        """

        return RetryClient(
            raise_for_status=False,
            headers={"User-Agent": UserAgent().random},
            retry_options=ExponentialRetry(attempts=3),
            timeout=aiohttp.ClientTimeout(
                total=10,  # Total request timeout in seconds
                connect=5,  # Connection timeout in seconds
            ),
        )

    @staticmethod
    def _is_undesired_url(url: str) -> bool:
        """
        Determine if a URL is undesired to be crawled based on its scheme and path.

        This method checks if the URL's scheme is in the list of undesired schemes
        or if its path ends with an undesired extension.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is undesired, False otherwise.
        """

        parsed_url = urlparse(url)

        # Check if the scheme of the URL is undesired to continue crawling
        if parsed_url.scheme in UNDESIRED_SCHEMES:
            return True

        # Check if the URL path ends with an undesired extension
        if any(
            parsed_url.path.endswith(extension) for extension in UNDESIRED_EXTENSIONS
        ):
            return True

        return False

    @staticmethod
    def _clean_href(href: str) -> str:
        """
        Clean and normalize a hyperlink reference (href).

        This method removes any fragment identifier, trims whitespace,
        and decodes URL-encoded characters in the href.

        Args:
            href (str): The hyperlink reference to clean.

        Returns:
            str: The cleaned and normalized href.
        """

        href = urldefrag(href).url  # Remove fragment identifier if present
        href = href.strip()  # Remove leading/trailing whitespace
        href = unquote(href)  # URL decode any encoded characters

        return href

    def __is_same_domain_url(self, url: str) -> bool:
        """
        Check if the given URL is on the same domain as the root URL.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is on the same domain as the root URL, False otherwise.
        """

        return urlparse(url).netloc == self.root_netloc
