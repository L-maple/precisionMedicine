# encoding:utf-8

from utils import get_clinical_files, get_doc_id
from es_interface import *


if __name__ == "__main__":
    clinical_files_dir = "/home/maple/IR/clinicaltrials_txt"
    medline_es = Elastic("medline", "medline_type", "127.0.0.1", 9200)
    for _, clinical_file in enumerate(get_clinical_files(clinical_files_dir)):
        with open(clinical_file) as cf:
            id = get_doc_id(clinical_file)
            medline_es.delete_index_data(id)







