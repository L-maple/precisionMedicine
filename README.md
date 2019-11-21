## IR -- 精准医疗信息检索大作业

### 小组成员：

**刘常杰，孙为民，万斯梦**

**项目地址：**https://github.com/L-maple/precisionMedicine



### 0. 背景

#### 0.1 实验目标

基于TREC 2018 Precision Medicine Track，学会使用一个信息检索系统完成给定的信息检索任务，包括创建索引、选择检索模型并设置参数、评价检索结果等等。

#### 0.2 信息检索系统选择

**Elasticsearch **

我们小组对Galago、Elasticsearch、Terrier、Anserini等搜索系统进行评估，以**开源**，**性能**, **易用性**，**可视化**, **企业应用普及性**等角度综合考虑，Elasticsearch作为高性能的开源搜索系统，简单易用，在企业得到广泛应用，值得信赖，最终选择Elasticsearch。

Terrier直接为TREC提供了接口？？

#### 0.3 物理设备准备

小型机：

i5八代 4核CPU；

8G 内存；

1T磁盘； 

#### 0.4 支持软件准备

（1）Ubuntu 18.04；

（2）Pycharm Community；

（3）Typora；



### 1. Elasticsearch+Kibana安装配置

**遇到的问题：**（1）源码下载慢；（2）直接在物理机上配置较复杂；

**安装配置变更：**选择容器安装，简单高效，2-3分钟便安装完成。

#### 1.1 Elasticsearch + Kibana的容器安装

因为直接在物理机上安装实在繁琐，而且软件下载速度极慢，因此便选择docker的安装方式，以下是在Linux上的安装：

##### 1.1.1 **Elasticsearch**的容器安装

```shell
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.4.2
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.4.2
```

##### 1.1.2 **Kibana的容器安装**

```shell
docker pull docker.elastic.co/kibana/kibana:7.4.2
docker run -d --link {YOUR_ELASTICSEARCH_CONTAINER_NAME_OR_ID}:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:7.4.2
```

##### 1.1.3 **Elasticsearch+Kibana的入门视频，同时借助官网博客来理解ES: **

Elasticsearch入门视频： https://www.elastic.co/webinars/getting-started-elasticsearch

Elasticsearch权威指南：https://www.elastic.co/guide/cn/elasticsearch/guide/current/index.html



### 2. 文件下载

**遇到的问题：** 

（1）文件直接下载即可，需要注意的是，直接下载txt或xml文件，而不需要两者都下载。

（2）手动解压，速度比较慢，10小时左右；

#### 2.1 数据集和查询集

##### 2.1.1 数据集

**Scientific Abstracts:** mdline_txt.tar.gz

作用：`The primary utility of abstracts for precision medicine is: will this abstract provide information relevant to the treatment of the patient’s cancer?`

**Clinical Trials:** clinicaltrials_txt.tar.gz

作用：`The primary utility of clinical trials for precision medicine is: is the patient eligible for this clinical trial?`

##### 2.1.2 查询集

**Topics:** topics2018.xml

#### 2.2 相关性判定文件

qrels-2018.zip

```shell
1 0 NCT00003911 0
1 0 NCT00016263 0
1 0 NCT00112216 0
1 0 NCT00260390 0
... ...
```

#### 2.3 Revelance guidance

对如何增强文档的关联性进行了介绍，具有启发性。



### 3.创建索引

**遇到的问题：**

（1）Elasticsearch单条索引创建很耗时，1天只能处理700k数据插入，bulk操作1天能处理14000k数据插入；

（2）为增强搜索关联性，对clinicaltrials_txt进行结构化处理；

#### 3.1 clinicaltrials_txt

##### 3.1.1 文档实例

```
TITLE:
Congenital Adrenal Hyperplasia: Calcium Channels as Therapeutic Targets

CONDITION:
Congenital Adrenal Hyperplasia

INTERVENTION:
Nifedipine

SUMMARY:
      This study will test the ability of extended release nifedipine (Procardia XL), a blood pressure medication
    
DETAILED DESCRIPTION:
      This protocol is designed to assess both acute and chronic effects of the calcium channel
    
ELIGIBILITY:
Gender: All
Age: 14 Years to 35 Years
Criteria:
        Inclusion Criteria:
          -  diagnosed with Congenital Adrenal Hyperplasia (CAH)
        Exclusion Criteria:
          -  history of liver disease, or elevated liver function tests

```

##### 3.1.2 结构化处理

先对文本数据进行结构化处理，这样可以增强关联性，对5项值进行判定：

1）content；2）gender；3）min_age；4）max_age；5）exclusion；

```
content:title condition summary inclusion, 
gender, 
min_age, 
max_age, 
exclusion
```

##### 3.1.3 clinicaltrials_txt索引创建核心代码

以文本名作为id，将结构化信息进行存储

```python
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
```

#### 3.2 abstracts

##### 3.2.1 abstracts索引创建核心代码

以文本的文件名作为id, 文本内容作为id对应的content信息；

```python
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
```

#### 3.3 topics

##### 3.3.1 xml文件处理

得到每个topic对应的字段信息：

```python
{
	'number': '50', 
	'disease': 'acute myeloid leukemia', 
	'gene': 'FLT3', 
	'age': 13, 
	'gender': 'male'
}
```

##### 3.3.2 核心代码

```python
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
```



### 4. 通过给topic中各字段加boost控制相关度

**遇到的困难：** 

(1) ES并没有内置加权模型，加权通过自己通过手动配置来实现，花了比较多的时间；

#### 4.1 **查询条件（带权重）核心代码: **

**query_conditions.py**

```python
def get_body(disease, disease_boost, gene, gene_boost, gender, gender_boost, age, age_boost):
    clinical_body = {
        "query": {
            "bool": {
                "should": [
                {
                    "match": {
                        "content": {
                            "query": disease,
                            "boost": disease_boost
                        }
                    }
                },
                {
                    "match": {
                        "content": {
                            "query": gene,
                            "boost": gene_boost
                        }
                    }
                },
                {
                    "bool": {
                        "should": [
                        {
                            "match": {
                                "gender": {
                                    "query": gender,
                                    "boost": gender_boost
                                }
                            }
                        },
                        {
                            "match": {
                                "gender": {
                                    "query": "all",
                                    "boost": gender_boost
                                }
                            }
                        }
                        ]
                    }
                },
                {
                    "bool": {
                        "must": [
                        {
                            "range": {
                                "min_age": {
                                    "lte": age,
                                    "boost": age_boost
                                }
                            }
                        },
                        {
                            "range": {
                                "max_age": {
                                    "gte": age,
                                    "boost": age_boost
                                }
                            }
                        }
                        ]
                    }
                }
                ]
            }
        }
    }
    return clinical_body
```

**param.config**

```python
{
    "clinical_medline": [
        {
            "param": [4, 3, 2, 1]
        },
        {
            "param": [3, 3, 2, 2]
        },
        {
            "param": [3, 3, 3, 1]
        },
        {
            "param": [5, 2, 2, 1]
        },
        {
            "param": [5, 3, 1, 1]
        },
        {
            "param": [6, 2, 1, 1]
        },
        {
            "param": [4, 4, 1, 1]
        },
        {
            "param": [3, 4, 2, 1]
        },
        {
            "param": [3, 4, 1, 2]
        },
        {
            "param": [4, 3, 1, 2]
        }
    ]
}
```



#### 4.2 加权检索结果（rank 1-1000）

##### 4.2.1 clinicaltrials

Example: clinical_trials_3322

```
1 Q0 NCT00405587 1 10.754394 3322
1 Q0 NCT01136967 2 10.531672 3322
1 Q0 NCT01597908 3 10.320544 3322
1 Q0 NCT01264380 4 10.304168 3322
1 Q0 NCT01928940 5 10.296316 3322
1 Q0 NCT01584648 6 10.110489 3322
1 Q0 NCT02202200 7 9.861431 3322
1 Q0 NCT01682083 8 9.799225 3322
1 Q0 NCT02130466 9 9.764382 3322
1 Q0 NCT01400451 10 9.697798 3322
1 Q0 NCT02416232 11 9.6823635 3322
1 Q0 NCT01586195 12 9.63162 3322
1 Q0 NCT01245062 13 9.630732 3322
1 Q0 NCT01942993 14 9.565079 3322
1 Q0 NCT01978236 15 9.458061 3322
1 Q0 NCT01897116 16 9.407016 3322
1 Q0 NCT01037127 17 9.37583 3322
。。。。。。
```

##### 4.2.2 medline_txt

Example: pubmed_abstracts_4321

```
1 Q0 27210749 1 13.658989 4321
1 Q0 22189819 2 13.618208 4321
1 Q0 26451873 3 13.516661 4321
1 Q0 26138035 4 13.447766 4321
1 Q0 25117819 5 13.361897 4321
1 Q0 17409425 6 13.350874 4321
1 Q0 25472943 7 13.312098 4321
1 Q0 23403819 8 13.296425 4321
1 Q0 16540682 9 13.284851 4321
1 Q0 27928645 10 13.255138 4321
1 Q0 27793752 11 13.191906 4321
1 Q0 25442222 12 13.181063 4321
1 Q0 26878440 13 13.138643 4321
1 Q0 22535154 14 13.126826 4321
1 Q0 ASCO_186257-199 15 13.091613 4321
1 Q0 22850568 16 13.048242 4321
1 Q0 23026937 17 13.0191555 4321
。。。。。。
```

### 5. 相关性评价

NDCG（Normalized Discounted Cumulative Gain）表示归一化折损累积增益。

MAP (Mean Average Precision)：就是说对一个叫Average Precision（AP）的东西取平均值。检测一个系统的性能，常用多个不同种类的查询对它进行测试，每个查询的结果都能计算出一个AP值，把所有AP取平均值就是系统的MAP。









