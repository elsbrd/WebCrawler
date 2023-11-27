import argparse
import asyncio

from crawler.main import WebCrawler


async def main():
    parser = argparse.ArgumentParser(description="WebCrawler CLI")
    parser.add_argument("root_url", help="Root URL to start crawling from")
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Concurrency limit for crawler (default: 5)",
    )

    args = parser.parse_args()

    crawler = WebCrawler(root_url=args.root_url, concurrency_limit=args.concurrency)
    await crawler.start()


if __name__ == "__main__":
    asyncio.run(main())
