# encoding:utf-8
# utils.py is used to deal with files

import os
import os.path
from time import sleep


# directory是clinicaltrials的目录，函数返回该目录中所有的txt文件名
def get_clinical_files(directory):
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
                for r_root, r_dirs, r_txts in os.walk(os.path.join(root, dir)):
                    for txt_name in r_txts:
                        yield os.path.join(r_root, txt_name)



# directory是extra_abstracts的目录,函数返回该目录中的所有txt文件名
def get_extra_abstracts_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


# 该函数返回medline_txt的目录中所有txt文件名
def get_medline_txt_files(directory):
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            for r_root, r_dirs, r_files in os.walk(os.path.join(root, dir)):
                for file in r_files:
                    # file_names.append(os.path.join(r_root, file))
                    yield os.path.join(r_root, file)


# 该函数返回绝对路径文件的无后缀文件名
def get_doc_id(file_path):
    dir_and_name = os.path.split(file_path)
    if len(dir_and_name) == 2:
        id_and_suffix = dir_and_name[1].split('.')
        if len(id_and_suffix) == 2:
            return id_and_suffix[0]


if __name__ == "__main__":
    # 对clinicaltrials获取文件名进行测试
    # count = 0
    # clinical_trials_dir = "/home/maple/IR/clinicaltrials_txt"
    # for _, file_name in enumerate(get_clinical_files(clinical_trials_dir)):
    #     id = get_doc_id(file_name)
    #     count += 1
    # print(count)

    # 对extra_abstracts获取文件名进行测试
    # count = 0
    # extra_abstracts_dir = "/home/maple/IR/extra_abstracts"
    # for _, extra_abstracts_file in enumerate(get_extra_abstracts_files(extra_abstracts_dir)):
    #     id = get_doc_id(extra_abstracts_file)
    #     print(id)
    #     count += 1
    # print(count)

    # 对medline_txt获取文件名并进行测试
    # count = 0
    # medline_txt_dir = "/home/maple/IR/medline_txt"
    # for _, medline_txt_file in enumerate(get_medline_txt_files(medline_txt_dir)):
    #     id = get_doc_id(medline_txt_file)
    #     print(id)
    #     count += 1
    # print(count)
    pass
