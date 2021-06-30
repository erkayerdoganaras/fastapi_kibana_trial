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
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from datetime import datetime



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
                "match": {
                    "kubernetes.namespace_name": {
                        "query": namespace,
                        "fuzziness": 0
                    }
                }
            }
        }
        results = helpers.scan(es, index=index, query=query_body)
        return results
    except:
        pass

@app.get("/logs/{index}/all/{pod_name}")
async def namespace(index:str,pod_name:str):
    try:

        query_body = {
            "query": {
                "match": {
                    "kubernetes.pod_name": {
                        "query": pod_name,
                        "fuzziness": 0
                    }
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
        
        query_body = {
            "query": {
                "match": {
                    "kubernetes.namespace_name": {
                        "query": namespace,
                        "fuzziness": 0
                    },
                    "kubernetes.pod_name": {
                        "query": pod_name,
                        "fuzziness": 0
                    }
                }
            }
        }




        results = helpers.scan(es, index=index, query=query_body)

        return results
    except:
        pass




"""query_body ={
  "query": {
      "match":{
          "kubernetes.namespace_name":{
              "query":"kube-system",
              "fuzziness":1
          }
      }
  }
}


results = helpers.scan(es, index="logstash-2021.06.30", query=query_body)
for i in results:
    print(i)"""
