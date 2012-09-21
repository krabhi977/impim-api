#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from tornado import httpclient

from images_api.handlers import HealthCheckHandler


class ImagesApplication(tornado.web.Application):

    def __init__(self):
        httpclient.AsyncHTTPClient.configure(
                'tornado.curl_httpclient.CurlAsyncHTTPClient')
        handlers = [
            (r'/healthcheck(?:/|\.html)?', HealthCheckHandler),
        ]
        super(ImagesApplication, self).__init__(handlers)
