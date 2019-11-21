## IR -- 精准医疗信息检索大作业

### 小组成员：

**刘常杰，孙为民，万斯梦**



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



### 4. 控制相关度

ES并没有内置检索模型，但可以在查询时修改相关度function的方式来控制相关度；

Example:

```json
GET /_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "title": {
              "query": "quick brown fox",
              "boost": 2 
            }
          }
        },
        {
          "match": { 
            "content": "quick brown fox"
          }
        }
      ]
    }
  }
}
```



### 5. 评价检索结果

 P@10：返回前10个结果的精确度。P英文为Precision。

MAP (Mean Average Precision)：就是说对一个叫Average Precision（AP）的东西取平均值。检测一个系统的性能，常用多个不同种类的查询对它进行测试，每个查询的结果都能计算出一个AP值，把所有AP取平均值就是系统的MAP。

##### 



困惑：如何得到相关性得分？



