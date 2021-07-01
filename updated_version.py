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
async def timestamp(index:str,namespace:str,gte:str=Query(None),lte:str=Query(None)):
    try:
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
                "gte": gte,
                "lte": lte

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
    
    






