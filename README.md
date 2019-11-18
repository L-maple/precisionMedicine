### 1. 环境配置

考虑到Elasticsearch的强大的全文搜索引擎，而且在企业中也得到广泛应用，因此便选择它来完成大作业。

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

##### 1.1.3 **Elasticsearch+Kibana的入门视频，同时借助网上博客来理解ES: **

Elasticsearch入门视频： https://www.elastic.co/webinars/getting-started-elasticsearch

Elasticsearch权威指南：https://www.elastic.co/guide/cn/elasticsearch/guide/current/index.html



### 2. 文件下载

#### 2.1 数据集和查询集

文件直接下载即可，需要注意的是，直接下载txt或xml文件，而不需要两者都下载。

##### 2.1.1 数据集

**Scientific Abstracts:** mdline_txt.tar.gz

作用：`The primary utility of abstracts for precision medicine is: will this abstract provide information relevant to the treatment of the patient’s cancer?`

**Clinical Trials:** clinicaltrials_txt.tar.gz

作用：`The primary utility of clinical trials for precision medicine is: is the patient eligible for this clinical trial?`

下载后，需要解压。1）手动全选解压；2）python解压；

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



### 3.对文件进行处理

这部分涉及代码部分



### 4.对elasticsearch进行操作

#### 4.1 组合多个过滤条件（Disease, Gene, Demographic, Other）

当需要过滤多个值和字段时，需要使用Elasticsearch中的bool过滤器，它可以接受多个其他过滤器作为参数，并将这些过滤器结合成各式各样的布尔（逻辑）组合。

一个 `bool` 过滤器由三部分组成：

```shell
{
   "bool" : {
      "must" :     [],
      "should" :   [],
      "must_not" : [],
   }
}
```

**`must`**

所有的语句都 *必须（must）* 匹配，与 `AND` 等价。

**`must_not`**

所有的语句都 *不能（must not）* 匹配，与 `NOT` 等价。

**`should`**

至少有一个语句要匹配，与 `OR` 等价。

**Example:**

```
GET /my_store/products/_search
{
 "query" : {
    "bool" : {
      "should" : [
         { "term" : {"price" : 20}}, 
         { "term" : {"productID" : "a"}} 
      ]
    }
  }
}
```

**参考博客**： https://www.elastic.co/guide/cn/elasticsearch/guide/current/combining-filters.html

#### 4.2 范围 (age range in ...)

Elasticsearch有range查询，不出所料的，可以用它来处理处于某个范围内的文档；

**Example：**

```
GET /my_store/products/_search
{
    "query" : {
      "range" : {
          "price" : {
              "gte" : 20,
              "lt"  : 40
          }
      }
  }
```

#### 4.3 处理NULL值

数据往往会有缺失字段，或有显式的空值或空数组。为了应对这些状况，Elasticsearch 提供了一些工具来处理空或缺失值。

##### 4.3.1 exists存在查询



困惑：如何得到相关性得分？



