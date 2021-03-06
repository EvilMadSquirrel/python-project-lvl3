"""Names module."""
import os
from typing import Optional
from urllib.parse import urlparse

from bs4.element import Tag
from page_loader.constants import DASH, DIR_SUFFIX, DOT, HTML_SUFFIX, SLASH


def to_file_or_dir(url: str, end: str = "") -> str:
    """Do make filename or directory name from URL, depends on end.

    Args:
        url (str): URL to make name
        end (str): Last few characters of name. Defaults to ''.

    Returns:
        str: Name of file or directory
    """
    parsed_url = urlparse(url)

    return "{0}{1}{2}".format(
        parsed_url.hostname.replace(DOT, DASH),
        parsed_url.path.replace(SLASH, DASH),
        end,
    )


def to_paths(output: str, url: str) -> tuple[str, str]:
    """Do make paths for output HTML file and directory for files.

    Args:
        output (str): Base output directory
        url (str): Web page URL

    Returns:
        tuple(str): Directory path, HTML file path
    """
    if output == "current":
        output_html_path = os.path.join(
            os.getcwd(),
            to_file_or_dir(url, HTML_SUFFIX),
        )
        files_dir_path = os.path.join(
            os.getcwd(),
            to_file_or_dir(url, DIR_SUFFIX),
        )
    else:
        output_html_path = os.path.join(
            output,
            to_file_or_dir(url, HTML_SUFFIX),
        )
        files_dir_path = os.path.join(output, to_file_or_dir(url, DIR_SUFFIX))
    return files_dir_path, output_html_path


def _is_same_domain(link_url: str, page_url: str) -> bool:
    parsed_link = urlparse(link_url)
    parsed_page = urlparse(page_url)
    return parsed_link.hostname == parsed_page.hostname


def to_url(link: str, url: str) -> Optional[str]:
    """Do generate url from 'src' or 'href' attribute.

    Args:
        link (str): Link from attribute
        url (str): Web page index URL

    Returns:
        str: URL to download some resource
    """
    if "jquery" in link:
        return None
    if urlparse(url).path == link:
        return url
    if not urlparse(link).scheme:
        scheme = urlparse(url).scheme
        host = urlparse(url).hostname
        return f"{scheme}://{host}{link}"
    if _is_same_domain(link, url):
        return link
    return None


def to_file_name(res_path: str, tag: Tag, base_url: str) -> str:
    """Do make file name for downloaded resource.

    Args:
        res_path (str): Source for file name
        tag (Tag): BeautifulSoup Tag
        base_url (str): Base URL for dir name

    Returns:
        str: Path to downloaded resource
    """
    if _is_same_domain(res_path, base_url):
        return to_file_or_dir(res_path)
    scheme = urlparse(base_url).scheme
    host = urlparse(base_url).hostname
    base_url = f"{scheme}://{host}"
    tail = res_path.replace(SLASH, DASH)
    if res_path == urlparse(base_url).path:
        res_path = to_file_or_dir(base_url)
    else:
        res_path = to_file_or_dir(base_url) + tail
    if tag.name == "link" and DOT not in res_path:
        res_path += HTML_SUFFIX
    return res_path
