# encoding:utf-8

from utils import get_clinical_files, get_doc_id
from time import sleep
import re


# content:title condition intervention summary inclusion detailed description, gender, min_age, max_age, exclusion
def content_handle(data):
    body = dict()
    content = re.search(r"TITLE:(\w+)ELIGIBILITY", data)[1]
    body["content"] = content.replace("\n", " ").lower()
    gender = re.search(r"Gender:\b*(\w+)\b")[1]
    body["gender"] = gender.lower()
    age = re.search(r"Age: (\d+).*?(\d+) Years")
    min_age = age.group(1)
    max_age = age.group(2)
    exclusion = re.search("Exclusion Criteria:(.*)")


if __name__ == "__main__":
    clinical_files_dir = "/home/maple/IR/clinicaltrials_txt"
    for _, clinical_file in enumerate(get_clinical_files(clinical_files_dir)):
        with open(clinical_file) as cf:
            id = get_doc_id(clinical_file)
            body = content_handle(cf.read())
            sleep(15)




