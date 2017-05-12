#!/usr/bin/env python
#coding:utf8
# 导入包
from elasticsearch import Elasticsearch
# ConnectionError 链接出现问题
# ConnectionTimeout 链接超时
from elasticsearch.exceptions import ConnectionError
from elasticsearch.exceptions import ConnectionTimeout
# resultInfo
resultInfo={501:'ok',502:'some data is moving',503:'some shard or node lost',504:'elasticsearch unkonow result',505:'connection timeout',506:'connection error',507:'unknown error',508:'import param empty'}
#from datetime import datetime
class MoniterElasticsearch(object):
    """
    封装Elasticsearch对象，用来获取集群状态。如果集群为red，或者出现异常需要告警。
    """
    def __init__(self,connectionParams):
        """
        es集群的链接信息，格式为 [{'host':'host1','port':'port1','timeout':'timeout1'},{'host':'host2','port':'port2','timeout':'timeout2'}]
        """
        self.connectionParams=connectionParams
        self.elasticsearchClient=Elasticsearch(self.connectionParams)
    def healthStatus(self):
        """
        判断是否有错误出现，集群是否可用
        501 正常
        502 集群内部数据存在正在同步的数据
        503 集群内分片缺失,某些节点没有启动
        504 默认状态，集群健康状况返回结果错误。
        505 连接超时(集群内某些节点响应变慢）
        506 不能连接集群
        507 未知错误
        """
        isHealth=504
        try:
            color=self.elasticsearchClient.cluster.health()['status']
            if color=='green':
                isHealth=501
            elif color=='yellow':
                isHealth=502
            elif color=='red':
                isHealth=503
            else:
                isHealth=504
        except ConnectionTimeout,ct:
            print '连接超时'
            print ct
            isHealth=505
        except ConnectionError,ce:
            print '连接出现错误'
            print ce
            isHealth=506
        except Exception,e:
            print '未知错误'
            print e
            isHealth=507
        return isHealth
    def getHealthStatus():
        None
#me=MoniterElasticsearch([{'host':'localhost','port':9202,'timeout':30},{'host':'localhost','port':9201,'timeout':30}])
#print me.healthStatus()
def exec_test_script(param):
    """
    param 的第一参数貌似是 ip:port的形式。第二个参数可以自行填写，因此关键在于第二个参数上
    第二个参数，必须是这样的格式：[{'host':'localhost','port':9202,'timeout':30},{'host':'localhost','port':9201,'timeout':30}]
    """
    if len(param) < 2 or len(param[1])<=0:
        return 508, "input params empty."
    # 转字典
    hosts=eval(param[1])
    print hosts
    me=MoniterElasticsearch(hosts)
    errorcode=me.healthStatus()
    return errorcode,resultInfo[errorcode]
def main():
    param=('localhost:9200',"[{'host':'localhost','port':9202,'timeout':30},{'host':'localhost','port':9201,'timeout':30}]")
    print exec_test_script(param)
if __name__ == '__main__':
    main()
