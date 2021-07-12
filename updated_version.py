from elasticsearch import Elasticsearch,helpers
from datetime import datetime
from elasticsearch_dsl import Search
import time
import datetime
import os,sys
import json
import pandas as pd
import numpy as np
import requests
from typing import List
from fastapi import FastAPI, Depends,Query
from pydantic import BaseModel, Field
from datetime import datetime
import os
import sys
import timestamp
from datetime import timedelta



app = FastAPI()
es=Elasticsearch(['http://168.119.224.222:32072'])

@app.get("/logs/{index}")
async def log_index(index:str):
    try:
        liste = []
        results = helpers.scan(es, index=index, query={"query": {"match_all": {}}})
        for item in results:
            liste.append(item['_source']["log"])
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":liste}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@app.get("/logs/{index}/{namespace}")
async def namespace(index:str,namespace:str):
    try:

        query_body = {

            "query": {
    "bool": {
      "must":
        {
          "match_phrase": {
            "kubernetes.namespace_name": {
              "query": namespace
            }
          }
        },
      "filter": [
        {
          "match_all": {}
        }
      ],
      "should": [],
      "must_not": []
    }
  }
        }
        results = helpers.scan(es, index=index, query=query_body)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":results}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@app.get("/logs/{index}/all/{pod_name}")
async def namespace(index:str,pod_name:str):
    try:

        query_body = {
        "query": {
    "bool": {
      "must":
        {
          "match_phrase": {
            "kubernetes.pod_name": {
              "query": pod_name
            }
          }
        },
      "filter": [
        {
          "match_all": {}
        }
      ],
      "should": [],
      "must_not": []
    }
  }
        }
        results = helpers.scan(es, index=index, query=query_body)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":results}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@app.get("/logs/{index}/{namespace}/{pod_name}")
async def namespace(index:str,pod_name:str,namespace:str):
    try:
        liste=[]
        liste = []
        query_body = {

              "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "kubernetes.namespace_name": {
              "query": namespace
            }
          }
        },
        {
          "match_phrase": {
            "kubernetes.pod_name": {
              "query": pod_name
            }
          }
        },

      ],
      "filter": [
        {
          "match_all": {}
        }
      ],
      "should": [],
      "must_not": []
    }
  },
        }




        results = helpers.scan(es, index=index, query=query_body)

        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":results}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }
    
    
@app.get("/time/{index}/{namespace}")
async def timestamp(index:str,namespace:str,gte:datetime=Query(None),lte:datetime=Query(None)):
    try:
        jte=gte - timedelta(hours=3)
        bte = lte - timedelta(hours=3)
        query_body ={

    "query": {
        "bool": {
        "must": [
             {
                "match_phrase": {
                      "kubernetes.namespace_name": {
                          "query": namespace
                    }
                }
            },
            {
            "range": {
                "@timestamp": {
                "gte": jte.strftime("%Y-%m-%d"'T'"%H:%M:%S"),
                "lte": bte.strftime("%Y-%m-%d"'T'"%H:%M:%S")

                }
            }
            },
        ],
        "filter": [
            {
            "match_all": {}
            }
        ],
        "should": [],
        "must_not": []
        }
    }
        }
        results = helpers.scan(es, index=index, query=query_body)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":results}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }
    
    
@app.get("/logs/{index}/ns/{namespace_name}/sort")
async def sort_page(index:str,namespace_name:str,er:int=Query(None)):
    try:
        liste = []
        if er!=None:

            formula=(int(er)*100-100)
        elif er==None:
            formula=0
        query_trial = {
            "from": formula,
            "size": 100,
            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "kubernetes.namespace_name": {
                                    "query": namespace_name

                                }
                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        res=es.search(index=index,body=query_trial)
        data=res["hits"]["hits"]

        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":data}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }
    
    
@app.get("/log/{index}/container/{containername}") #logs yazıldığı zaman null dönüyor
async def container(index:str,containername:str):
    try:
        query_trial = {

            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "kubernetes.container_name": {
                                    "query": containername

                                }
                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        res=helpers.scan(es,index=index,query=query_trial)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

    
@app.get("/events")
async def eventslist():
    try:
        liste=[]
        results = helpers.scan(es, index="kube-events", query={"query": {"match_all": {}}})
        for item in results:
            liste.append(item["_source"])
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":liste}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@app.get("/events/{namespace}")
async def eventslist(namespace:str):
    try:
        query_trial = {

            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "metadata.namespace": {
                                    "query": namespace

                                }
                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        res=helpers.scan(es,index="kube-events",query=query_trial)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }


@app.get("/events/kindof/{kind}")
async def involvedObject_kind(kind:str):
    try:
        query_trial = {

            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "involvedObject.kind": {
                                    "query": kind

                                }
                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        res=helpers.scan(es,index="kube-events",query=query_trial)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@app.get("/events/nameof/{name}")
async def involvedObject_name(name:str):
    try:
        query_trial = {

            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "involvedObject.name": {
                                    "query": name

                                }
                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        res=helpers.scan(es,index="kube-events",query=query_trial)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@app.get("/events/typeof/{type}")
async def typeof(type:str):
    try:
        query_trial = {

            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "type": {
                                    "query": type

                                }
                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        res=helpers.scan(es,index="kube-events",query=query_trial)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }


@app.get("/events/reason/{reason}")
async def typeof(reason:str):
    try:
        query_trial = {

            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "reason": {
                                    "query": reason

                                }
                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        res=helpers.scan(es,index="kube-events",query=query_trial)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@app.get("/events/message/{message}")
async def typeof(message:str):
    try:
        query_trial = {

            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "message": {
                                    "query": message

                                }
                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        res=helpers.scan(es,index="kube-events",query=query_trial)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@app.get("/event-time/")
async def event_time(gte:datetime=Query(None),lte:datetime=Query(None)):
    try:
        jte = gte - timedelta(hours=3)
        bte = lte - timedelta(hours=3)


        query={
    "query": {
        "bool": {
          "must": [
            {
              "range": {
                "firstTimestamp": {
                  "format": "strict_date_optional_time",
                  "gte":jte.strftime("%Y-%m-%d"'T'"%H:%M:%S"),
                "lte": bte.strftime("%Y-%m-%d"'T'"%H:%M:%S")
                }
              }
            }
          ],
          "filter": [
            {
              "match_all": {}
            }
          ],
          "should": [],
          "must_not": []
        }
      }}
        res = helpers.scan(es, index="kube-events", query=query)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":res}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

#THIS PART TAKES A LONG TIME WHEN GETTING ALL "LOGSTASH INDEXED" DATA
@app.get("/logstash/all")
async def arama():
    try:
        query_body = {

            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "_index":{
                                    "query":"logstash*"}


                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        results = helpers.scan(es ,query=query_body)
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":results}
    except:
        except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }
    
@app.get("/logstash/all/paginated")
async def arama(*,er:int=Query(None)):
    try:
        liste1 = []
        if er != None:

            formula = (int(er) * 100 - 100)
        elif er == None:
            formula = 0


        query_body = {
            "from":formula,
            "size":100,
            "query": {
                "bool": {
                    "must":
                        {
                            "match_phrase": {
                                "_index":{
                                    "query":"logstash*"}


                            }
                        },
                    "filter": [
                        {
                            "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }


        liste=[]
        res = es.search(body=query_body)
        data = res["hits"]["hits"]
      
        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":data}


    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }   
    
@app.get("/logstash/number-queries")
async def log_num():
    try:
        liste1=[]
        query_body2 = {
        "query": {
            "bool": {
                "must":
                    {
                        "match_phrase": {
                            "_index": {
                                "query": "logstash*"}

                        }
                    },
                "filter": [
                    {
                        "match_all": {}
                    }
                ],
                "should": [],
                "must_not": []
            }
        }
    }

        res = es.count(body=query_body2)["count"]
        return {
                "status":"SUCCESS",
                "message":"DONDU",
                "data":res} 
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }
