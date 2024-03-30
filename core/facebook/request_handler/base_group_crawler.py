
from abc import ABCMeta


class BaseGroupCrawler(object, metaclass=ABCMeta):
    def __init__(self):
        super(BaseGroupCrawler, self).__init__()

    def collect_data(self, **kwargs):
        """Collect data"""

    def transform_data(self, **kwargs):
        """Transform data"""
