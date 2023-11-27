from unittest.mock import AsyncMock, Mock, patch
from urllib.parse import urlparse

import pytest
from aiohttp_retry import RetryClient

from crawler.constants import UNDESIRED_EXTENSIONS, UNDESIRED_SCHEMES
from crawler.main import WebCrawler
from crawler.utils import AtomicSet
from tests.constants import EXAMPLE_URL


@pytest.fixture
def crawler():
    return WebCrawler(EXAMPLE_URL)


class TestCrawler:
    @pytest.mark.asyncio
    async def test_init_with_custom_concurrency_limit(self):
        root_url = "http://example.com"
        concurrency_limit = 10

        crawler = WebCrawler(root_url, concurrency_limit)

        assert crawler.root_url == root_url
        assert crawler.root_netloc == urlparse(root_url).netloc
        assert crawler._semaphore._value == concurrency_limit

    @pytest.mark.asyncio
    async def test_init_with_default_concurrency_limit(self):
        root_url = "http://example.com"

        crawler = WebCrawler(root_url)

        assert crawler.root_url == root_url
        assert crawler.root_netloc == urlparse(root_url).netloc
        assert crawler._semaphore._value == 5

    @pytest.mark.asyncio
    async def test_visited_urls_initialization(self, crawler):
        assert isinstance(crawler._visited_urls, AtomicSet)

    @pytest.mark.asyncio
    @patch("crawler.main.WebCrawler.crawl", new_callable=AsyncMock)
    @patch("crawler.main.logger")
    async def test_start_method(self, mock_logger, mock_crawl, crawler):
        await crawler.start()

        mock_crawl.assert_called_once_with(EXAMPLE_URL)

        mock_logger.info.assert_any_call(
            f"Crawling process is started for {EXAMPLE_URL}"
        )
        mock_logger.info.assert_any_call("Crawling process is finished.")

    # TODO: test crawl, test _fetch_url

    def test_extract_urls_success(self):
        html = """
        <html>
            <body>
                <a href="http://example.com/page1">Link 1</a>
                <a href="/page2">Link 2</a>
                <a href="https://external.com">External Link</a>
            </body>
        </html>
        """

        expected_urls = {"http://example.com/page1", "http://example.com/page2"}

        crawler = WebCrawler("http://example.com")
        extracted_urls = crawler._extract_urls(html)

        assert extracted_urls == expected_urls

    def test_extract_no_urls(self, crawler):
        html = "<html><body>No links here</body></html>"
        extracted_urls = crawler._extract_urls(html)

        assert extracted_urls == set()

    @patch("crawler.main.UserAgent")
    def test_create_session(self, mock_user_agent, crawler):
        user_agent = Mock(random="random-user-agent")
        mock_user_agent.return_value = user_agent

        session = crawler._create_session()

        # Assertions for session configuration
        assert isinstance(session, RetryClient)
        assert session._raise_for_status is False

        # Verify the User-Agent header
        headers = session._client.headers
        assert headers.get("User-Agent") == "random-user-agent"

        # Verify retry options
        retry_options = session.retry_options
        assert (
            retry_options.attempts == 3
        )  # Check for the correct number of retry attempts

        # Verify timeout settings
        timeout = session._client.timeout
        assert timeout.total == 10  # Check the total request timeout in seconds
        assert timeout.connect == 5  # Check the connection timeout in seconds

    @pytest.mark.parametrize("scheme", UNDESIRED_SCHEMES)
    def test_is_undesired_url_with_undesired_scheme(self, scheme, crawler):
        url = f"{scheme}://example.com/page"
        assert crawler._is_undesired_url(url) is True

    def test_is_undesired_url_with_desired_scheme(self, crawler):
        url = "http://example.com/page"
        assert crawler._is_undesired_url(url) is False

    @pytest.mark.parametrize("extension", UNDESIRED_EXTENSIONS)
    def test_is_undesired_url_with_undesired_extension(self, extension, crawler):
        url = f"http://example.com/page.{extension}"
        assert crawler._is_undesired_url(url) is True

    def test_is_undesired_url_with_desired_extension(self):
        url = "http://example.com/page.html"
        assert WebCrawler._is_undesired_url(url) is False

    def test_clean_href_remove_fragment_identifier(self, crawler):
        href = "http://example.com/page#section"
        cleaned_href = crawler._clean_href(href)
        assert cleaned_href == "http://example.com/page"

    def test_clean_href_remove_whitespace(self, crawler):
        href = "   http://example.com/page   "
        cleaned_href = crawler._clean_href(href)
        assert cleaned_href == "http://example.com/page"

    def test_clean_href_decode_url_encoded_characters(self, crawler):
        href = "http%3A%2F%2Fexample.com%2Fpage%20with%20spaces"
        cleaned_href = crawler._clean_href(href)
        assert cleaned_href == "http://example.com/page with spaces"

    def test_clean_href_no_changes_needed(self, crawler):
        href = "http://example.com/page"
        cleaned_href = crawler._clean_href(href)
        assert cleaned_href == href

    def test_is_same_domain_url_same_domain(self, crawler):
        url = "http://example.com/page"
        assert crawler._WebCrawler__is_same_domain_url(url) is True

    def test_is_same_domain_url_different_domain(self, crawler):
        url = "http://otherdomain.com/page"
        assert crawler._WebCrawler__is_same_domain_url(url) is False

    def test_is_same_domain_url_different_subdomain(self, crawler):
        url = "http://sub.example.com/page"
        assert crawler._WebCrawler__is_same_domain_url(url) is False

    def test_is_same_domain_url_different_scheme(self, crawler):
        url = "http://example.com/page"
        assert crawler._WebCrawler__is_same_domain_url(url) is True
