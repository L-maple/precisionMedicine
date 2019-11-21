import time
from os import walk
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class Elastic:
    def __init__(self, index_name,index_type, ip="127.0.0.1", port=9200):
        self.index_name = index_name
        self.index_type = index_type
        self.es = Elasticsearch([ip], port=port)

    def delete_index(self):
        self.es.indices.delete(index=self.index_name, ignore=[400, 404])

    def index_data(self, id, body):
        res = self.es.index(index=self.index_name, id=id, doc_type=self.index_type, body=body)
        print(res)

    def bulk_index_data_for_abstracts(self, ids, contents):
        body = list()
        for i in range(len(ids)):
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_id": ids[i],
                "_source": {
                    "content": contents[i]["content"]
                }
            }
            body.append(action)
        success, _ = bulk(self.es, body, index=self.index_name, raise_on_error=True)

    def bulk_index_data_for_clinicaltrials(self, ids, contents):
        body = list()
        for i in range(len(ids)):
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_id": ids[i],
                "_source": {
                    "content": contents[i]["content"],
                    "gender": contents[i]["gender"],
                    "min_age": contents[i]["min_age"],
                    "max_age": contents[i]["max_age"],
                    "exclusion": contents[i]["exclusion"]
                }
            }
            body.append(action)
        success, _ = bulk(self.es, body, index=self.index_name, raise_on_error=True)

    def delete_index_data(self, id):
        self.es.delete(index=self.index_name, doc_type=self.index_type, id=id)

    def get_data_id(self, id):
        res = self.es.get(index=self.index_name, doc_type=self.index_type, id=id)
        print(res)

        # # 输出查询到的结果
        # for hit in res['hits']['hits']:
        #     print(hit['_source']['date'],hit['_source']['source'],hit['_source']['link'],hit['_source']['keyword'],hit['_source']['title'])

    def get_data_by_body(self, body):
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=body)

        # for hit in _searched['hits']['hits']:
        #     print hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'], \
        #     hit['_source']['title']
