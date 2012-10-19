#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

from impim_api.domain import ElasticSearchParser
from impim_api.infrastructure.elastic_search import SearchRequestBody
from impim_api.infrastructure.elastic_search import Urls


class Images(object):

    def __init__(self, config, http_client=AsyncHTTPClient()):
        self._http_client = http_client
        self._elastic_search_urls = Urls(config=config)
        self._elastic_search_parser = ElasticSearchParser()

    @gen.engine
    def all(self, callback, **query_arguments):
        images_dict = yield gen.Task(self._es, **query_arguments)
        # images_dict['thumbs'] = self._thumb_urls.cropped_to_sizes(query_arguments.get('thumb_sizes'))
        images_dict['pageSize'] = query_arguments.get('page_size')
        callback(images_dict)

    @gen.engine
    def _es(self, callback, **query_arguments):
        elastic_search_request = self._build_elastic_search_request(**query_arguments)
        elastic_search_response = yield gen.Task(self._http_client.fetch, elastic_search_request)
        images_dict = self._elastic_search_parser.parse_images_from_search(elastic_search_response.body)
        callback(images_dict)

    def _build_elastic_search_request(self, **query_arguments):
        url = self._elastic_search_urls.search_url(Urls.IMAGE_TYPE)

        search_request_body = SearchRequestBody()
        search_request_body.from_index((query_arguments.get('page') - 1) * query_arguments.get('page_size'))
        search_request_body.size(query_arguments.get('page_size'))
        if query_arguments.get('q'):
            search_request_body.query_string(query_arguments.get('q'))
        if query_arguments.get('created_date_from'):
            search_request_body.range('createdDate').gte(query_arguments.get('created_date_from').isoformat())
        if query_arguments.get('created_date_to'):
            search_request_body.range('createdDate').lte(query_arguments.get('created_date_to').isoformat())
        if query_arguments.get('event_date_from'):
            search_request_body.range('eventDate').gte(query_arguments.get('event_date_from').isoformat())
        if query_arguments.get('event_date_to'):
            search_request_body.range('eventDate').lte(query_arguments.get('event_date_to').isoformat())
        search_request_body.sort([{'_score': 'desc'}, {'createdDate': {'order': 'desc', 'ignore_unmapped': True}}])

        return HTTPRequest(url, body=search_request_body.as_json(), allow_nonstandard_methods=True)
