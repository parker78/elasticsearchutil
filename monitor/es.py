#!/usr/bin/env python
#coding:utf8
from elasticsearch import Elasticsearch
# connection error
from elasticsearch.exceptions import ConnectionError
# connect timeout error
from elasticsearch.exceptions import ConnectionTimeout
# resultInfo
resultInfo={501:'ok',502:'some data is moving',503:'some shard or node lost',504:'elasticsearch unkonow result',505:'connection timeout',506:'connection error',507:'unknown error',508:'import param empty'}
#from datetime import datetime
class MoniterElasticsearch(object):
    """
    use elasticsearch object to get cluster status，judge weather to send message
    """
    def __init__(self,connectionParams):
        """
        parameters formmat is [{'host':'host1','port':'port1','timeout':'timeout1'}]
        """
        self.connectionParams=connectionParams
        self.elasticsearchClient=Elasticsearch(self.connectionParams)
    def healthStatus(self):
        """
        get status, to find return result meanings you should see resultInfo.
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
            print ct
            isHealth=505
        except ConnectionError,ce:
            print ce
            isHealth=506
        except Exception,e:
            print e
            isHealth=507
        return isHealth
    def getHealthStatus():
        None
#me=MoniterElasticsearch([{'host':'localhost','port':9202,'timeout':30},{'host':'localhost','port':9201,'timeout':30}])
#print me.healthStatus()
def exec_test_script(param):
    if len(param) < 2 or len(param[1])<=0:
        return 508, "input params empty."
#    print '----------------'
#    print param
    hosts=eval(param[1])
#    print hosts
    me=MoniterElasticsearch(hosts)
    errorcode=me.healthStatus()
    return errorcode,resultInfo[errorcode]
def main():
    param=('localhost:9200',"[{'host':'192.168.57.98','port':9202,'timeout':30},{'host':'192.168.57.98','port':9201,'timeout':30}]")
    print exec_test_script(param)
if __name__ == '__main__':
    main()
