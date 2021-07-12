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

@router.get("/")
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

@router.get("/{namespace}")
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

@router.get("/kindof/{kind}")
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

@router.get("/nameof/{name}")
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

@router.get("/typeof/{type}")
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

@router.get("/reason/{reason}")
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

@router.get("/message/{message}")
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

@router.get("/event-time/")
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


