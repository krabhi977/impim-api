#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.web import asynchronous

from tapioca import ResourceHandler

from images_api.domain.images import Images
from images_api.handlers.extract_arguments_mixin import ExtractArgumentsMixin


class ImagesResourceHandler(ResourceHandler, ExtractArgumentsMixin):

    def __init__(self, *args, **kwarsg):
        super(ImagesResourceHandler, self).__init__(*args, **kwarsg)
        self.images_storage = Images(config=self.application.config)

    @asynchronous
    @gen.engine
    def get_collection(self, callback, *args):
        accepted_arguments = [
            ('q', str, None),
            ('created_date_from', 'datetime', None),
            ('created_date_to', 'datetime', None),
            ('event_date_from', 'datetime', None),
            ('event_date_to', 'datetime', None),
            ('page', int, 1),
            ('page_size', int, 10)
        ]
        arguments = self.extract_arguments(accepted_arguments)
        images_dict = yield gen.Task(self.images_storage.all, **arguments)
        callback(images_dict)
