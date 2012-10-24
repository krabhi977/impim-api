#!/usr/bin/env python
# -*- coding: utf-8 -*-


from mock import MagicMock
from tornado.testing import AsyncTestCase

from impim_api.domain import Images
from impim_api.domain import ThumborUrlService
from impim_api.domain.storage import ElasticSearch

from tests.support import MockConfig


class ImagesTestCase(AsyncTestCase):

    def setUp(self):
        super(ImagesTestCase, self).setUp()
        
        config = MockConfig()
        self._storage = ElasticSearch(config=config)
        self._thumbor_url_service = ThumborUrlService(config=config)
        self._images = Images(config=config, storage=self._storage, thumbor_url_service=self._thumbor_url_service)

    def test_all_should_return_thumb_urls(self):
        self._all_mocks()
        self._images.all(
            self._all_should_return_thumb_urls,
            thumb_sizes=['200x100'],
            page=1,
            page_size=10
        )
        self.wait()

    def _all_should_return_thumb_urls(self, response):
        assert response['items'][0]['thumbs']['200x100'] == 'http://localhost:8888/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        self.stop()

    def test_all_should_return_page_size(self):
        self._all_mocks()
        self._images.all(self._all_should_return_page_size_callback, page=1, page_size=10)
        self.wait()

    def _all_should_return_page_size_callback(self, response):
        assert response['pageSize'] == 10
        self.stop()

    def test_add_should_store_image(self):
        self._storage.store = MagicMock()
        self._images.add(title=u'image title')
        self._storage.store.assert_called_with(
            title=u'image title',
            url='s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
        )


    def _all_mocks(self):
        self._storage.search = MagicMock(side_effect=lambda callback, **query_arguments: callback({
            'items': [{'url': 's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'}]
        }))
        self._thumbor_url_service.fit_in_urls = MagicMock(return_value={'200x100': 'http://localhost:8888/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'})
