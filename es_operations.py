from utils import *
from elasticsearch import Elasticsearch
from time import sleep
from es_interface import *


def medline_index_data_run():
    # 将medline_txt中的所有文本都添加到
    medline_es = Elastic("medline", "medline_type")
    # medline_es.delete_index()
    medline_txt_dir = "/home/maple/IR/medline_txt"
    count = 1
    ids = list()
    bodies = list()
    for _, medline_txt_file in enumerate(get_medline_txt_files(medline_txt_dir)):
        id = get_doc_id(medline_txt_file)
        with open(medline_txt_file) as tf:
            content = tf.read()
            bodies.append({"content": content})
        ids.append(id)
        if count % 10000 == 0:
            print ("start, ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            medline_es.bulk_index_data(ids, bodies)
            ids.clear()
            bodies.clear()
            print(count, "'s lines has been inserted.")
            print("end, ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        count += 1
    for i in range(len(ids)):
        medline_es.index_data(ids[i], dict({"content": bodies[i]}))
    print(count, "'s lines has been inserted.")


def extra_abstracts_index_data_run():
    count = 0
    # 将medline_txt中的所有文本都添加到
    extra_abstracts_es = Elastic("medline", "medline_type", "127.0.0.1", 9300)
    extra_abstracts_dir = "/home/maple/IR/extra_abstracts"
    for _, extra_abstracts_file in enumerate(get_extra_abstracts_files(extra_abstracts_dir)):
        with open(extra_abstracts_file) as ef:
            id = get_doc_id(extra_abstracts_file)
            content = ef.read()
            time.sleep(100)
            extra_abstracts_es.index_data(id, dict({"content": content}))
            count += 1
    print(count)


if __name__ == "__main__":
    medline_index_data_run()
    # extra_abstracts_index_data_run()
    pass







