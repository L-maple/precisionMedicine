from utils import *
from elasticsearch import Elasticsearch
from time import sleep
from es_interface import *


def extra_abstracts_index_data_run():
    count = 1
    extra_abstracts_es = Elastic("medline", "medline_type", "127.0.0.1", 9200)
    extra_abstracts_dir = "/home/maple/IR/extra_abstracts"
    ids = list()
    contents = list()
    for _, extra_abstracts_file in enumerate(get_extra_abstracts_files(extra_abstracts_dir)):
        id = get_doc_id(extra_abstracts_file)
        ids.append(id)
        with open(extra_abstracts_file) as ef:
            content = ef.read()
            contents.append({"content": content})
        if count % 1000 == 0:
            print ("start, ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            extra_abstracts_es.bulk_index_data(ids, contents)
            ids.clear()
            contents.clear()
            print(count, "'s lines has been inserted.")
            print("end, ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        count += 1
    for i in range(len(ids)):
        extra_abstracts_es.index_data(ids[i], contents[i])
    print(count)


if __name__ == "__main__":
    # extra_abstracts_index_data_run()  已经插入
    pass