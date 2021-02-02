import os
import threading
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


class Crawler(threading.Thread):
    def __init__(self, url, depth, folder_path):
        self.url = url
        self.depth = depth
        self.folder_path = folder_path

        self.css_path = os.path.join(self.folder_path, "./styles")
        self.js_path = os.path.join(self.folder_path, "./scripts")
        self.img_path = os.path.join(self.folder_path, "./img")

        self.base_url = os.path.dirname(self.url)
        self.start_filename = os.path.basename(self.url)
        if not self.start_filename:
            self.start_filename = "index.html"

        self.visited_pages = []
        self.visited_file_urls = []

        self._file_threads = []

        threading.Thread.__init__(self)

    def _is_absolute(self, url):
        return bool(urlparse(url).netloc)

    def _clear_relative_url(self, url):
        return "/" + url.replace("../", "").replace("./", "")

    def _get(self, base_url):
        session = requests.Session()
        try:
            response = session.get(base_url)
        except:
            return None
        return response.text if response.status_code == 200 else None

    def _save_file(self, data, path, filename):
        Path(path).mkdir(parents=True, exist_ok=True)

        page_path = os.path.join(path, filename)
        try:
            with open(page_path, 'wb') as file:
                file.write(data)
        except:
            pass

    def _parse_links(self, soup, parse_url, current_depth, path):
        links = soup.find_all("a")
        for link in links:
            href = link.get("href", None)
            if href:
                if not self._is_absolute(href):
                    # determine new relative path for file
                    t_href = os.path.normpath(href)
                    rel_path = os.path.join(path, t_href)
                    # make link to a next page
                    href = urljoin(parse_url, href)
                else:
                    if self.base_url in href:
                        rel_path = href.replace(self.base_url, "")
                    else:
                        rel_path = urlparse(self.base_url).path

                d_file = os.path.split(rel_path)[1]
                if "." in d_file:
                    folder_path = os.path.dirname(rel_path)
                    link_filename = os.path.basename(rel_path)
                else:
                    folder_path = rel_path
                    link_filename = "index.html"

                self._parse(href, link_filename, current_depth + 1, path=folder_path)

    def _parse_file_url(self, current_url, src):
        if self._is_absolute(src):
            if self.base_url in src:
                src = src.replace(self.base_url, "")

        path, filename = os.path.split(urlparse(src).path)
        path = self._clear_relative_url(path)
        src = urljoin(current_url, src)
        return src, path, filename

    def _download(self, file_url, path, filename):
        try:
            r = requests.get(file_url)
            if r.status_code == 200:
                self._save_file(r.content, path, filename)
        except:
            pass

    def _download_file(self, file_url, path, filename):
        thread = Thread(target=self._download, args=(file_url, path, filename))
        thread.start()
        self._file_threads.append(thread)

    def _save_asset(self, soup, tag, tag_url, path_folder, parse_url):
        tags = soup.find_all(tag)
        for _tag in tags:
            _tag_src = _tag.get(tag_url, None)
            if _tag_src:
                src, path, filename = self._parse_file_url(parse_url, _tag_src)
                if src not in self.visited_file_urls:
                    self._download_file(src, path_folder+path, filename)
                    self.visited_file_urls.append(src)

    def _save_assets(self, soup, parse_url):
        self._save_asset(soup, "img", "src", self.img_path, parse_url)
        self._save_asset(soup, "link", "href", self.css_path, parse_url)
        self._save_asset(soup, "script", "src", self.js_path, parse_url)

    def _parse(self, parse_url, filename, current_depth, path="/"):
        # download page
        page_data = self._get(parse_url)
        if not page_data:
            return

        # check if url already was
        if parse_url in self.visited_pages:
            return
        self.visited_pages.append(parse_url)

        soup = BeautifulSoup(page_data, features="html.parser")

        # save css/js/imges
        self._save_assets(soup, parse_url)

        # save html
        dir_page = self.folder_path + path
        self._save_file(soup.prettify('utf-8'), dir_page, filename)

        # parse urls in page
        if self.depth >= current_depth+1:
            self._parse_links(soup, parse_url, current_depth, path)

    def _start_parse(self):
        assert self.url is not None, "Url not setup."
        assert self.folder_path is not None, "Folder path not setup."

        Path(self.folder_path).mkdir(parents=True, exist_ok=True)
        Path(self.css_path).mkdir(parents=True, exist_ok=True)
        Path(self.js_path).mkdir(parents=True, exist_ok=True)
        Path(self.img_path).mkdir(parents=True, exist_ok=True)

        self._parse(self.url, self.start_filename, 0)

    def run(self):
        self._start_parse()

        while True in [thread.is_alive() for thread in self._file_threads]:
            pass
