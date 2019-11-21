# encoding:utf-8

from utils import get_clinical_files, get_doc_id
from es_interface import *
from time import sleep
import re



# content:title condition intervention summary inclusion detailed description, gender, min_age, max_age, exclusion
def content_handle(data):
    body = dict()

    # 1. content
    content = ""
    content_list = re.findall(r"(TITLE:.*?)ELIGIBILITY:", data, re.S)
    if len(content_list) == 1:
        content = content_list[0]
    inclusion = ""
    inclusion_list = re.findall(r"(Inclusion Criteria:.*)Exclusion Criteria", data, re.S)
    if len(inclusion_list) == 1:
        inclusion = inclusion_list[0]
    content = content + " " + inclusion
    body["content"] = ' '.join(content.lower().split())

    # 2. gender
    gender = "all"
    gender_list = re.findall(r"Gender: (\w+)\b", data)
    if len(gender_list) == 1:
        gender = gender_list[0].lower()
    body["gender"] = gender

    # 3. min_age, max_age
    min_age = 0
    max_age = 100
    age_list = re.findall(r"Age: (\d+).*?(\d+) Years", data)
    if len(age_list) == 1:
        min_age = age_list[0][0]
        max_age = age_list[0][1]
    body["min_age"] = min_age
    body["max_age"] = max_age

    # 4. exclusion
    exclusion = ""
    exclusion_list = re.findall("(Exclusion Criteria:.*)", data, re.S)
    if len(exclusion_list) == 1:
        exclusion = exclusion_list[0]
    body["exclusion"] = ' '.join(exclusion.split())

    return body


if __name__ == "__main__":
    clinical_files_dir = "/home/maple/IR/clinicaltrials_txt"
    bodies = list()
    ids = list()
    count = 1
    clinicaltrials_es = Elastic("clinicaltrials", "clinicaltrials_type", "127.0.0.1", 9200)
    for _, clinical_file in enumerate(get_clinical_files(clinical_files_dir)):
        with open(clinical_file) as cf:
            id = get_doc_id(clinical_file)
            body = content_handle(cf.read())
            # print(id)
            # print(body["content"],'\n',
            #       body["gender"], '\n',
            #       body["min_age"], '\n',
            #       body["max_age"], '\n',
            #       body["exclusion"])
            bodies.append(body)
            ids.append(id)
        if count % 4000 == 0:
            print("start, ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            clinicaltrials_es.bulk_index_data_for_clinicaltrials(ids, bodies)
            print(count, "'s lines has been inserted.")
            print("end, ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            ids.clear()
            bodies.clear()
        count += 1
    print("start, ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    clinicaltrials_es.bulk_index_data_for_clinicaltrials(ids, bodies)
    print(count, "'s lines has been inserted.")
    print("end, ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))





