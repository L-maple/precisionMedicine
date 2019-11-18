from utils import *
from elasticsearch import Elasticsearch
from time import sleep
from es_interface import *


if __name__ == "__main__":
    # 将medline_txt中的所有文本都添加到
    medline_es = Elastic("medline", "medline_type")
    medline_txt_dir = "/home/maple/IR/medline_txt"
    count = 0
    for _, medline_txt_file in enumerate(get_medline_txt_files(medline_txt_dir)):
        id = get_doc_id(medline_txt_file)
        with open(medline_txt_file) as tf:
            content = tf.read()
            medline_es.index_data(id, dict({"content": content}))
            # medline_es.get_data_id(id)
            count += 1
    print(count)






