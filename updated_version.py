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

@app.get("/logs")
async def get_logs():
    try:
        liste= []
        results = helpers.scan(es, index="logstash-2021.06.26", query={"query": {"match_all": {}}})
        for item in results:
            liste.append(item['_source']["log"])
        return liste
    except:
        pass


@app.get("/logs/{index}")
async def log_index(index:str):
    try:
        liste = []
        results = helpers.scan(es, index=index, query={"query": {"match_all": {}}})
        for item in results:
            liste.append(item['_source']["log"])
        return liste
    except:
        pass

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
        return results
    except:
        pass

"""@app.get("/logs/{index}/{pod_id}")
async def pod_id(pod_id:str,index:str):
    try:
        liste=[]
        query_body = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "kubernetes.pod_id": pod_id

                        }
                    }
                }
            }
        }
        results = helpers.scan(es, index=index, query=query_body)
        for item in results:
            liste.append(item)
        return liste

    except:
        pass"""

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
        return results
    except:
        pass

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

        return results
    except:
        pass
    
    
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
        return results
    except:
        pass
    
    
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

        for i in data:
            liste.append(i)

        return liste
    except:
        pass
    
    
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
        return res
    except:
        pass

    
@app.get("/events")
async def eventslist():
    try:
        liste=[]
        results = helpers.scan(es, index="kube-events", query={"query": {"match_all": {}}})
        for item in results:
            liste.append(item["_source"])
        return liste
    except:
        pass

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
        return res
    except:
        pass


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
        return res
    except:
        pass

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
        return res
    except:
        pass

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
        return res
    except:
        pass


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
        return res
    except:
        pass

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
        return res
    except:
        pass



