# encoding:utf-8

from xml.dom.minidom import parse
import xml.dom.minidom
from es_interface import *
import re


def get_topics_json(directory):
    topics_list = []
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(directory)
    topics = DOMTree.documentElement
    if topics.hasAttribute("task"):
        print("Task : %s" % topics.getAttribute("task"))

    # 在集合中获取所有topic任务
    topic_elements = topics.getElementsByTagName("topic")

    # 收集每个topic的详细信息
    for topic_element in topic_elements:
        topic_dict = {}

        number = topic_element.getAttribute("number")
        disease = topic_element.getElementsByTagName('disease')[0].childNodes[0].data
        gene = topic_element.getElementsByTagName('gene')[0].childNodes[0].data
        demographic = topic_element.getElementsByTagName('demographic')[0].childNodes[0].data

        topic_dict["number"] = number
        topic_dict["disease"] = disease
        topic_dict["gene"] = gene
        topic_dict["demographic"] = demographic
        topic_dict["age"] = int(re.match("(\\d+)-year", demographic).group(1))
        topic_dict["gender"] = re.match(".*old (\\w+)", demographic).group(1)
        # print(topic_dict["age"], topic_dict["gender"])
        topics_list.append(topic_dict)
    return topics_list


if __name__ == "__main__":
    topics = get_topics_json("topics2018.xml")
    clinicaltrials_es = Elastic("clinicaltrials", "clinicaltrials_type", "127.0.0.1", 9200)
    for _, topic in enumerate(topics):
        print(topic["number"], topic["disease"], topic["gene"], topic["age"], topic["gender"])
        

