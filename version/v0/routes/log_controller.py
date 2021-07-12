from typing import Optional

from fastapi import APIRouter
from datetime import datetime
import time
from fastapi import FastAPI, Depends,Query
import timestamp
from datetime import timedelta
import requests
from elasticsearch import Elasticsearch,helpers
from pydantic import BaseModel, Field
router = APIRouter()
es=Elasticsearch(['http://168.119.224.222:32072'])

@router.get("/{index}")
async def get_logs(index:str):
    try:
        liste= []
        results = helpers.scan(es, index=index, query={"query": {"match_all": {}}})
        for item in results:
            liste.append(item['_source']["log"])
        return liste
    except:
        pass

@router.get("/{index}/{namespace}")
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
            "message": "DONMEDI "+str(e),
            }

@router.get("/{index}/all/{pod_name}")
async def pod_name(index:str,pod_name:str):
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

@router.get("/{index}/{namespace}/{pod_name}")
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

@router.get("/log/{index}/time/{namespace}")
async def timestamp(index:str,namespace:str,gte:datetime=Query(None),lte:datetime=Query(None)):
    try:
        liste=[]
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
        results = helpers.scan(es,index=index, query=query_body)


        return {
            "status":"SUCCESS",
            "message":"DONDU",
            "data":results}
    except Exception as e:
        return {
            "status": "FAILURE",
            "message": "DONMEDI"+str(e)
        }

@router.get("/{index}/ns/{namespace_name}/sort")
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

@router.get("/log/{index}/container/{containername}")
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

