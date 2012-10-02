#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads
from unittest import TestCase

from images_api.alpha.domain import ElasticSearchParser

class ElasticSearchParserTestCase(TestCase):
    
    def setUp(self):
        self._es_parser = ElasticSearchParser()
    
    def test_parse_images_from_search(self):
        es_json = """
            {
              "took" : 2,
              "timed_out" : false,
              "_shards" : {
                "total" : 5,
                "successful" : 5,
                "failed" : 0
              },
              "hits" : {
                "total" : 1,
                "max_score" : 1.0,
                "hits" : [ {
                  "_index" : "images-api",
                  "_type" : "image",
                  "_id" : "Ngpkqld6T0SftZpL6KnMhA",
                  "_score" : 1.0,
                  "_source" : {
                    "assunto": "Istambul; Salve Jorge",
                    "imagemAtual": false,
                    "id": "http://novelas.be.globoi.com/photo/4d7e5b0ba6634faaa9bb0d0547d48c6e/solr",
                    "thumbUrl": "http://local.globo.com:8888/SGVhWvXVXH4HvduSL1f01ZWj6b16SKVBoC59rDy3Nm5YXWVN3JkSEoOsXwy0SRop/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg",
                    "creditos": "Salve Jorge/TV Globo",
                    "url": "s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg",
                    "dataCadastro": "2012-09-24T14:12:12",
                    "largura": 940,
                    "dataEvento": "2012-09-24T14:12:12",
                    "titulo": "Istambul é a única cidade no mundo que fica em dois continentes: Europa e Ásia",
                    "altura": 588
                  }
                } ]
              }
            }
        """
        
        parsed = self._es_parser.parse_images_from_search(es_json)
        
        assert parsed['total'] == 1
        assert len(parsed['items']) == 1
        assert parsed['items'][0]['assunto'] == "Istambul; Salve Jorge"
        assert parsed['items'][0]['imagemAtual'] == False
        assert parsed['items'][0]['id'] == "http://novelas.be.globoi.com/photo/4d7e5b0ba6634faaa9bb0d0547d48c6e/solr"
        assert parsed['items'][0]['thumbUrl'] == "http://local.globo.com:8888/SGVhWvXVXH4HvduSL1f01ZWj6b16SKVBoC59rDy3Nm5YXWVN3JkSEoOsXwy0SRop/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg"
        assert parsed['items'][0]['creditos'] == u"Salve Jorge/TV Globo"
        assert parsed['items'][0]['url'] == "s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg"
        assert parsed['items'][0]['dataCadastro'] == "24/09/2012"
        assert parsed['items'][0]['largura'] == 940
        assert parsed['items'][0]['dataEvento'] == "24/09/2012"
        assert parsed['items'][0]['titulo'] == u"Istambul é a única cidade no mundo que fica em dois continentes: Europa e Ásia"
        assert parsed['items'][0]['altura'] == 588