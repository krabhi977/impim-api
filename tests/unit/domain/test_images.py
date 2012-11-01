#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from os.path import dirname, join

from mock import ANY, MagicMock, patch
from tornado.testing import AsyncTestCase

from impim_api.domain import Images

from tests.support import MockConfig


class ImagesTestCase(AsyncTestCase):

    def setUp(self):
        super(ImagesTestCase, self).setUp()
        
        config = MockConfig()
        self._images_storage = MagicMock()
        self._meta_data_storage = MagicMock()
        self._thumbor_url_service = MagicMock()
        self._images = Images(config=config, images_storage=self._images_storage, meta_data_storage=self._meta_data_storage, thumbor_url_service=self._thumbor_url_service)

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

    def _all_mocks(self):
        self._meta_data_storage.search = MagicMock(side_effect=lambda callback, **query_arguments: callback({
            'items': [{'url': 's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'}]
        }))
        self._thumbor_url_service.fit_in_urls = MagicMock(return_value={'200x100': 'http://localhost:8888/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'})

    def test_add_should_store_image(self):
        with patch('impim_api.domain.images.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2012, 10, 25, 18, 55, 0)
            self._images_storage.store_image = MagicMock(side_effect=lambda callback, image={}, meta_data={}: callback(
                'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
            ))
            self._meta_data_storage.store_meta_data = MagicMock(side_effect=lambda callback, **image_meta_data: callback())
            
            self._images.add(self._add_should_store_image_callback, meta_data={'title': u'image title'})
            self.wait()

    def _add_should_store_image_callback(self):
        self._images_storage.store_image.assert_called_with(callback=ANY)
        self._meta_data_storage.store_meta_data.assert_called_with(
            callback=ANY,
            title=u'image title',
            created_date=datetime(2012, 10, 25, 18, 55, 0),
            url='http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
        )
        self.stop()

    def test_get(self):
        with open(join(dirname(__file__), '..', '..', 'fixtures/image.jpeg'), 'r') as image_file:
            image_body = image_file.read()
        self._images_storage.fetch_image_by_key = MagicMock(return_value=image_body)

        self._images.get(self._get_callback, key='key') == image_body

    def _get_callback(self, actual_image_body):
        with open(join(dirname(__file__), '..', '..', 'fixtures/image.jpeg'), 'r') as image_file:
            image_body = image_file.read()
        assert actual_image_body == image_body
