#!/usr/bin/env python
# -*- coding: utf-8 -*-


from libthumbor import CryptoURL
from tornado import gen

from impim_api.domain.storage import ElasticSearch


class ThumborUrlService(object):
    
    def __init__(self, config):
        self._config = config
    
    # TODO: get thumbor security key from config.
    def fit_in_urls(self, original_url, sizes):
        crypto = CryptoURL(key='MY_SECURE_KEY')
        urls = {}
        for size in sizes:
            split_size = size.split('x')
            path = crypto.generate(image_url=original_url, width=split_size[0], height=split_size[1], fit_in=True)
            urls[size] = self._config.THUMBOR_SERVER_URL.rstrip('/') + path
        return urls
