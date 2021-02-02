import shutil
import threading

from .crawler import Crawler


class Loader(threading.Thread):
    def __init__(self, url, depth, path):
        self.url = url
        self.depth = depth
        self.path = path

        threading.Thread.__init__(self)

    def run(self):
        crawler = Crawler(self.url, self.depth, self.path)
        crawler.start()
        crawler.join()

        shutil.make_archive(self.path, 'zip', self.path)
