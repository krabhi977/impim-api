#!/usr/bin/env python
# -*- coding: utf-8 -*-


import derpconf.config as config
from derpconf.config import Config


Config.define('JSONP_CALLBACK', 'impimCallback', 'Default callback for JSONP responses.', 'General')

Config.define('ELASTIC_SEARCH_BASE_URL', 'http://localhost:9200', 'ElasticSearch base url.', 'ElasticSearch')
Config.define('ELASTIC_SEARCH_INDEX', 'impim', 'ElasticSearch index.', 'ElasticSearch')

Config.define('FILE_STORAGE_ROOT_PATH', '/tmp/impim-api', 'File Storage root path.', 'File Storage')

Config.define('THUMBOR_SECURITY_KEY', 'MY_SECURE_KEY', 'Thumbor security key.', 'Thumbor configuration')
Config.define('THUMBOR_SERVER_URL', 'http://localhost:8888/', 'Thumbor server url.', 'Thumbor configuration')


def generate_config():
    config.generate_config()


if __name__ == '__main__':
    generate_config()
